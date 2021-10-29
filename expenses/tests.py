import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Record


class IndexViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

        self.client.login(
            username='testuser',
            password='secret'
        )
    
    def test_add_record_succeed(self):
        response = self.client.post(reverse('expenses:index'), {
            'date': '2021-10-21',
            'category': 'Test category',
            'sum': 100
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'submitted.html')

        record = Record.objects.get(id=1)
        self.assertEqual(record.date, datetime.date(2021, 10, 21))
        self.assertEqual(record.category, 'Test category')
        self.assertEqual(record.sum, 100)
    
    def test_add_record_invalid_date(self):
        response = self.client.post(reverse('expenses:index'), {
            'date': '2021-13-04',
            'category': 'Test category',
            'sum': 100
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_add_record_invalid_category(self):
        response = self.client.post(reverse('expenses:index'), {
            'date': '2021-10-21',
            'category': 'C' * 31,
            'sum': 100
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
       
    def test_add_record_invalid_sum(self):
        response = self.client.post(reverse('expenses:index'), {
            'date': '2021-10-21',
            'category': 'Test category',
            'sum': '100i'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class HistoryViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

        self.client.login(
            username='testuser',
            password='secret'
        )

        self.records = [
            Record(date=datetime.date(2021, 10, 1), category='Category 1', sum=10),
            Record(date=datetime.date(2021, 10, 1), category='Category 2', sum=20),
            Record(date=datetime.date(2021, 10, 2), category='Category 1', sum=30),
        ]

        for record in self.records:
            record.save()
        self.records.sort(key=lambda r: r.time, reverse=True)
    
    def test_history_view_last_5_records(self):
        response = self.client.get(reverse('expenses:history'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'history.html')

        context = response.context
        self.assertTrue('object_list' in context.keys())
        self.assertListEqual(list(context['object_list']), self.records)
    
    def test_history_view_last_2_records(self):
        response = self.client.get(reverse('expenses:history'), data={
            'count': 2
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'history.html')

        context = response.context
        self.assertTrue('object_list' in context.keys())
        self.assertListEqual(list(context['object_list']), self.records[:2])
    
    def test_history_view_invalid_records_count(self):
        response = self.client.get(reverse('expenses:history'), data={
            'count': 'nan'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'history.html')

        context = response.context
        self.assertTrue('object_list' in context.keys())
        self.assertListEqual(list(context['object_list']), self.records)


class RecordDetailViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

        self.client.login(
            username='testuser',
            password='secret'
        )

        self.record = Record.objects.create(
            date=datetime.date(2021, 10, 21),
            category='Category',
            sum=100
        )
    
    def test_show_record_detail_view(self):
        response = self.client.get(reverse('expenses:record', args=[self.record.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'record.html')

        context = response.context
        self.assertTrue('object' in context.keys())
        self.assertEqual(context['object'], self.record)
    
    def test_show_record_detail_view_404(self):
        response = self.client.get(reverse('expenses:record', args=[1000]))

        self.assertEqual(response.status_code, 404)
    
    def test_update_record_succeed(self):
        response = self.client.post(reverse('expenses:record', args=[self.record.id]), data={
            'date': '2021-10-22',
            'category': 'New category',
            'sum': 200
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'record.html')

        context = response.context
        self.assertTrue('object' in context.keys())
        self.assertEqual(context['object'], self.record)
    
    def test_update_record_invalid_date(self):
        prev_date = self.record.date

        response = self.client.post(reverse('expenses:record', args=[self.record.id]), {
            'date': '2021-13-04',
            'category': str(self.record.category),
            'sum': self.record.sum
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'record.html')
        self.assertEqual(self.record.date, prev_date)

    def test_update_record_invalid_category(self):
        prev_category = self.record.category

        response = self.client.post(reverse('expenses:record', args=[self.record.id]), {
            'date': str(self.record.date),
            'category': 'C' * 31,
            'sum': self.record.sum
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'record.html')
        self.assertEqual(self.record.category, prev_category)
       
    def test_update_record_invalid_sum(self):
        prev_sum = self.record.sum

        response = self.client.post(reverse('expenses:record', args=[self.record.id]), {
            'date': str(self.record.date),
            'category': str(self.record.category),
            'sum': '100i'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'record.html')
        self.assertEqual(self.record.sum, prev_sum)


class StatsViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

        self.client.login(
            username='testuser',
            password='secret'
        )

        self.records = [
            Record(date=datetime.date(2021, 10, 1), category='Category 1', sum=10),
            Record(date=datetime.date(2021, 10, 1), category='Category 2', sum=20),
            Record(date=datetime.date(2021, 10, 2), category='Category 1', sum=30),
            Record(date=datetime.date(2021, 10, 10), category='Category 3', sum=15),
            Record(date=datetime.date(2021, 10, 3), category='Category 1', sum=45),
        ]

        for record in self.records:
            record.save()
    
    def test_stats_view_entire_month(self):
        response = self.client.get(reverse('expenses:stats'), data={
            'begin_date': '2021-10-01',
            'end_date': '2021-10-31',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stats.html')

        expected_stats = dict()
        for record in self.records:
            if record.category not in expected_stats:
                expected_stats[record.category] = 0
            expected_stats[record.category] += record.sum
        
        context = response.context
        self.assertTrue('records' in context.keys())
        self.assertTrue('total' in context.keys())
        self.assertTrue('form' in context.keys())

        self.assertDictEqual(expected_stats, {category: total for (category, total) in context['records']})
        self.assertEqual(sum(expected_stats.values()), context['total'])
        self.assertEqual(context['form'].data['begin_date'], '2021-10-01')
        self.assertEqual(context['form'].data['end_date'], '2021-10-31')
    
    def test_stats_view_empty_stats(self):
        response = self.client.get(reverse('expenses:stats'), data={
            'begin_date': '2021-10-20',
            'end_date': '2021-10-31',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stats.html')
        
        context = response.context
        self.assertTrue('records' in context.keys())
        self.assertTrue('total' in context.keys())
        self.assertTrue('form' in context.keys())

        self.assertDictEqual({category: total for (category, total) in context['records']}, dict())
        self.assertEqual(context['total'], 0)
        self.assertEqual(context['form'].data['begin_date'], '2021-10-20')
        self.assertEqual(context['form'].data['end_date'], '2021-10-31')

    def test_stats_view_invalid_begin_date(self):
        response = self.client.get(reverse('expenses:stats'), data={
            'begin_date': '2021-13-01',
            'end_date': '2021-10-31',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stats.html')
        
        context = response.context
        self.assertTrue('records' in context.keys())
        self.assertTrue('total' in context.keys())
        self.assertTrue('form' in context.keys())

        self.assertDictEqual({category: total for (category, total) in context['records']}, dict())
        self.assertEqual(context['total'], 0)
        self.assertTrue('begin_date' not in context['form'].data.keys())
        self.assertTrue('end_date' not in context['form'].data.keys())

    def test_stats_view_invalid_end_date(self):
        response = self.client.get(reverse('expenses:stats'), data={
            'begin_date': '2021-10-01',
            'end_date': '2021-13-31',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stats.html')
        
        context = response.context
        self.assertTrue('records' in context.keys())
        self.assertTrue('total' in context.keys())
        self.assertTrue('form' in context.keys())

        self.assertDictEqual({category: total for (category, total) in context['records']}, dict())
        self.assertEqual(context['total'], 0)
        self.assertTrue('begin_date' not in context['form'].data.keys())
        self.assertTrue('end_date' not in context['form'].data.keys())

    def test_stats_view_no_begin_date(self):
        response = self.client.get(reverse('expenses:stats'), data={
            'end_date': '2021-10-31',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stats.html')
        
        context = response.context
        self.assertTrue('records' in context.keys())
        self.assertTrue('total' in context.keys())
        self.assertTrue('form' in context.keys())

        self.assertDictEqual({category: total for (category, total) in context['records']}, dict())
        self.assertEqual(context['total'], 0)
        self.assertTrue('begin_date' not in context['form'].data.keys())
        self.assertTrue('end_date' not in context['form'].data.keys())

    def test_stats_view_no_end_date(self):
        response = self.client.get(reverse('expenses:stats'), data={
            'begin_date': '2021-10-01',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stats.html')
        
        context = response.context
        self.assertTrue('records' in context.keys())
        self.assertTrue('total' in context.keys())
        self.assertTrue('form' in context.keys())

        self.assertDictEqual({category: total for (category, total) in context['records']}, dict())
        self.assertEqual(context['total'], 0)
        self.assertTrue('begin_date' not in context['form'].data.keys())
        self.assertTrue('end_date' not in context['form'].data.keys())
    
    def test_stats_view_inversed_date_range(self):
        response = self.client.get(reverse('expenses:stats'), data={
            'begin_date': '2021-10-31',
            'end_date': '2021-10-01'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stats.html')
        
        context = response.context
        self.assertTrue('records' in context.keys())
        self.assertTrue('total' in context.keys())
        self.assertTrue('form' in context.keys())

        self.assertDictEqual({category: total for (category, total) in context['records']}, dict())
        self.assertEqual(context['total'], 0)
        self.assertEqual(context['form'].data['begin_date'], '2021-10-31')
        self.assertEqual(context['form'].data['end_date'], '2021-10-01')
