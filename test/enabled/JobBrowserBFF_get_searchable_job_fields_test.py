from JobBrowserBFF.TestBase import TestBase

class JobBrowserBFFTest(TestBase):
    def test_get_searchable_job_fields_happy(self):
        try:
            ret = self.getImpl().get_searchable_job_fields(self.getContext())
        except Exception as ex:
           self.assertTrue(False, 'Did not expect an exception: ' + str(ex.message))
           return

        self.assertIsInstance(ret, list)
        result = ret[0]
        self.assertIsInstance(result, dict)
        self.assertIn('searchable_job_fields', result)
        searchable_job_fields = result.get('searchable_job_fields')
        self.assertIsInstance(searchable_job_fields, list)
