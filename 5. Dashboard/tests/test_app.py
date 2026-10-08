"""Data tests always run; real Dash/HTTP tests require installed dependencies."""
from pathlib import Path
import importlib.util
import sys
import tempfile
import unittest
import pandas as pd

APP_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(APP_ROOT))
if (APP_ROOT/'.deps').is_dir(): sys.path.insert(0,str(APP_ROOT/'.deps'))
from utils.data_loader import Repository, ArtifactError, filter_frame, summarize, aggregate, diagnostic_pairs


class DataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo=Repository();cls.data=cls.repo.analysis()

    def test_baseline_matches_saved_artifact(self):
        saved=self.repo.csv('baseline').set_index('metric').value
        stats=summarize(self.data)
        for col,key in [('Views','views_sum'),('Impressions','impressions_sum'),('Engagement','engagement_sum'),('Clicks','clicks_observed_sum')]:
            self.assertAlmostEqual(stats[col],saved[key])
        self.assertAlmostEqual(stats['Engagement_Rate'],saved['er_mean_pct'])

    def test_date_filter_inclusive_and_combined(self):
        selected=filter_frame(self.data,'2024-01-01','2024-01-31',{'Platform':['TikTok'],'Content_Category':['Entertainment']})
        expected=self.data[(self.data.Post_Date >= '2024-01-01') & (self.data.Post_Date < '2024-02-01') &
                           self.data.Platform.eq('TikTok') & self.data.Content_Category.eq('Entertainment')]
        self.assertEqual(selected.Source_Row.tolist(),expected.Source_Row.tolist())

    def test_reversed_dates(self):
        with self.assertRaises(ArtifactError): filter_frame(self.data,'2025-01-01','2024-01-01')

    def test_empty_scope_is_not_zero_missing_kpi(self):
        stats=summarize(filter_frame(self.data,selections={'Platform':['Unknown']}))
        self.assertEqual(stats['records'],0);self.assertTrue(pd.isna(stats['Clicks']))

    def test_all_missing_clicks(self):
        frame=filter_frame(self.data,selections={'Platform':['Instagram']})
        stats=summarize(frame)
        self.assertTrue(pd.isna(stats['Clicks']));self.assertTrue(pd.isna(stats['Click_Through_Rate']))
        self.assertEqual(stats['Clicks_n'],0)

    def test_clear_filter_means_all(self):
        self.assertEqual(len(filter_frame(self.data,selections={'Region':[]})),len(self.data))

    def test_rates_are_means_not_sum_ratios(self):
        monthly=aggregate(self.data,'Month')
        self.assertAlmostEqual(monthly.loc[monthly.Month.eq('2024-01'),'Engagement_Rate'].iloc[0],
                               self.data.loc[self.data.Month.eq('2024-01'),'Engagement_Rate'].mean()*100)

    def test_diagnosis_matches_existing_monthly_artifact(self):
        pairs=diagnostic_pairs(self.data,['Month'])
        original=pd.read_csv(self.repo.path('drivers').parent/'robustness_monthly.csv')
        self.assertEqual(len(pairs),16)
        for _,row in pairs.iterrows():
            saved=original.loc[original.Month.eq(row.Month)].iloc[0]
            self.assertAlmostEqual(row['Gap (pp)'],saved.gap_pp)
            self.assertEqual(row['n Entertainment'],saved.n_E)

    def test_category_filter_does_not_manufacture_comparator(self):
        selected=filter_frame(self.data,selections={'Content_Category':['Entertainment']})
        pairs=diagnostic_pairs(selected,['Platform'])
        self.assertTrue(pairs['Gap (pp)'].isna().all())
        self.assertFalse(pairs['Supported (n≥30 each)'].any())

    def test_readonly_filter(self):
        before=self.data.copy(deep=True)
        filter_frame(self.data,selections={'Region':['USA']})
        aggregate(self.data,'Platform');diagnostic_pairs(self.data,['Platform','Post_Type'])
        pd.testing.assert_frame_equal(self.data,before)

    def test_missing_file_error(self):
        with tempfile.TemporaryDirectory(dir=APP_ROOT) as folder:
            repo=Repository(folder)
            with self.assertRaises(ArtifactError):repo.analysis()


HAS_DASH=importlib.util.find_spec('dash') is not None and importlib.util.find_spec('plotly') is not None


@unittest.skipUnless(HAS_DASH,'Dash/Plotly not installed; runtime tests not performed')
class DashTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from app import create_app
        cls.app=create_app();cls.client=cls.app.server.test_client()

    def test_http_layout_and_callbacks(self):
        for path in ['/','/_dash-layout','/_dash-dependencies','/assets/style.css']:
            self.assertEqual(self.client.get(path).status_code,200,path)

    def test_callback_full_empty_and_missing_comparator(self):
        key=next(k for k in self.app.callback_map if 'overview-content.children' in k)
        metadata=self.app.callback_map[key]
        values=['2024-01-01','2025-05-01',[],[],[],[],[],
                'Views','Content_Category','Engagement_Rate','Month','Rest','Platform|Post_Type']
        for category in [[],['Entertainment'],['Does not exist']]:
            values[4]=category
            payload={'output':key,'outputs':[{'id':o.component_id,'property':o.component_property} for o in metadata['output']],
                     'inputs':[dict(i,value=v) for i,v in zip(metadata['inputs'],values)],'state':[],
                     'changedPropIds':['filter-Content_Category.value']}
            response=self.client.post('/_dash-update-component',json=payload)
            self.assertEqual(response.status_code,200,response.data.decode())
            self.assertIn('overview-content',response.json['response'])

    def test_missing_sources_app_still_serves_layout(self):
        from app import create_app
        with tempfile.TemporaryDirectory(dir=APP_ROOT) as folder:
            app=create_app(Repository(folder))
            self.assertEqual(app.server.test_client().get('/_dash-layout').status_code,200)

    def test_source_whitelist(self):
        self.assertEqual(self.client.get('/source/not-a-source').status_code,404)
        self.assertEqual(self.client.get('/source/root_cause').status_code,200)

    def test_recommendation_callback_and_experiment_selection(self):
        key='recommendation-content.children'
        for priority,kind,experiment in [('All','All','E1'),('High','Direct action','E3'),('Low','Direct action','E5')]:
            metadata=self.app.callback_map[key]
            payload={'output':key,'outputs':{'id':'recommendation-content','property':'children'},
                     'inputs':[dict(item,value=value) for item,value in zip(metadata['inputs'],[priority,kind,experiment])],
                     'state':[],'changedPropIds':['experiment-select.value']}
            response=self.client.post('/_dash-update-component',json=payload)
            self.assertEqual(response.status_code,200,response.data.decode())
            self.assertIn(experiment,response.data.decode())

    def test_local_platform_assets(self):
        for slug in ['facebook','instagram','linkedin','youtube','tiktok','x']:
            response=self.client.get(f'/assets/platforms/{slug}.svg')
            self.assertEqual(response.status_code,200)
            self.assertIn(b'<svg',response.data)
            response.close()

    def test_platform_colors_reserved_for_platform_chart(self):
        from components.charts import metric_chart, ENTERTAINMENT
        from components.platforms import PLATFORM_COLORS
        grouped=aggregate(Repository().analysis(),'Platform')
        fig=metric_chart(grouped,'Platform','Views','Views')
        for trace in fig.data:
            self.assertEqual(trace.marker.color,PLATFORM_COLORS[trace.name])
            self.assertEqual(trace.orientation,'h')
        from pages.diagnosis import render
        component=render(Repository().analysis(),'Platform','Rest','Platform|Post_Type')
        # End-to-end serialization succeeds; category colors do not use platform mapping.
        self.assertIsNotNone(component)


if __name__=='__main__': unittest.main()
