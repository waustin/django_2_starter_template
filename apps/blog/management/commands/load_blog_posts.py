# encoding: utf-8
import datetime
import os
import csv
import bleach
import string
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify
from django.db import transaction

from blog.models import Post, Category


class Command(BaseCommand):
    help = 'Loads blog posts from old website dabase export .csv'

    def add_arguments(self, parser):
        parser.add_argument('inputfile', nargs='+',
                            help='Input filename .csv')
        parser.add_argument('--delete',
                            action='store_true',
                            dest='delete',
                            default=False,
                            help='Delete exising blog posts before loading data')

    def clean_body(self, body):

        # NEW ARCHIVE IMG PATH
        new_archive_img_path = "/uploads/old-blog/"

        # Sanitize HTML
        ALLOWED_TAGS = bleach.ALLOWED_TAGS + [u'p', u'span', u'br', u'h1', u'h2', u'h3', u'h4', u'h5', u'sup',
                                              u'img', u'u', u'table', 'tbody', 'td', 'tr', 'hr', 'iframe']

        ALLOWED_ATTRIBUTES = bleach.ALLOWED_ATTRIBUTES
        ALLOWED_ATTRIBUTES['img'] = ['src', 'alt']

        body = bleach.clean(body,
                            tags=ALLOWED_TAGS,
                            attributes=ALLOWED_ATTRIBUTES,
                            strip=True)

        soup = BeautifulSoup(body, 'html.parser')

        # clean img src link
        for img in soup.findAll('img'):
            src = img.attrs['src']
            filename = os.path.basename(src)
            img.attrs['src'] = "{0}{1}".format(new_archive_img_path, filename)

        return soup

    def process_row(self, row):
        # Add Blog Category
        category_name = row['catName']
        category_slug = row['catAlias']

        try:
            cat = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            cat = Category.objects.create(name=category_name, slug=category_slug)


        title = row['titleTag']

        replace_chars = [
            ("\xe2", "'"),
            ("\x91", "'"),
            ("\x92", "'"),
            ("\x93", "'"),
            ("\x94", "'"),
            ("\x97", " "),
        ]

        for c in replace_chars:
            title = title.replace(c[0], c[1])

        slug = slugify(title)[:30]

        # Convert Pub Date
        pub_date = datetime.datetime.strptime(row['datePosted'][:-4],
                                              "%Y-%m-%d  %H:%M:%S")

        print u" --> {0}, {1}, {2}".format(title, slug, pub_date)

        # Clean body
        cleaned_body = self.clean_body(row['body'])

        post = Post(title=title,
                    slug=slug,
                    publish_date=pub_date,
                    content=cleaned_body,
                    is_published=True)
        post.save()
        post.categories.add(cat)


    @transaction.atomic()
    def process_data_file(self, ifile):
        cnt = 0

        self.category_set = set()

        with open(ifile) as csvfile:
            postreader = csv.DictReader(csvfile)
            for row in postreader:
                # skip bad empty row
                if row['titleTag'] == '':
                    continue

                self.process_row(row)
                cnt = cnt + 1
        return cnt

    def handle(self, *args, **options):
        if options['delete']:
            self.stdout.write('Deleting existing blog posts and categories')
            Post.objects.all().delete()
            Category.objects.all().delete()

        inputfilename = options['inputfile'][0]

        if not os.path.exists(inputfilename):
            raise CommandError("Inputfile name does not exist {0}".format(inputfilename))

        self.stdout.write('Processing {0}'.format(inputfilename))

        rec_cnt = self.process_data_file(inputfilename)

        self.stdout.write('Successfully imported blog. Processed {0} records'.format(rec_cnt))
