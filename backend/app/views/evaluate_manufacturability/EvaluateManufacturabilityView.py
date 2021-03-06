"""Bla."""

from base64 import b64decode, b64encode
from matplotlib.backends.backend_pdf import PdfPages

from rest_framework import serializers
from ..base import AsyncWorker, StartJobView, JobResult
from ..tools import (records_from_data_file,
                     matplotlib_figure_to_svg_base64_data)
from io import BytesIO
from dnachisel.reports import plot_sequence_manufacturability_difficulties


class FileSerializer(serializers.Serializer):
    name = serializers.CharField()
    content = serializers.CharField()

class serializer_class(serializers.Serializer):
    report = serializers.CharField()
    files = serializers.ListField(child=FileSerializer())
    show_features = serializers.BooleanField()

class worker_class(AsyncWorker):

    def work(self):

        data = self.data
        PDF_REPORT = (data.report == "pdf_report")
        figures = []
        for f in data.files:
            self.logger(message='Processing file %s' % f.name)
            # self.set_progress_message('Processing file %s' % f.name)
            records, fmt = records_from_data_file(f)
            for (i, record) in enumerate(records):

                axes = plot_sequence_manufacturability_difficulties(
                    record if data.show_features else str(record.seq).upper())
                figure = axes[0].figure
                name = f.name if (len(records) == 1) else f.name + ("%03d" % i)
                name = name + "--" + record.name[:40]
                figure.suptitle(name)
                figures.append((name, figure))

        self.logger(message='Generating report')
        print ("AAAA", len(figures))

        if PDF_REPORT:
            pdf_io = BytesIO()

            with PdfPages(pdf_io) as pdf:
                for fig in figures:
                    pdf.savefig(fig, bbox_inches="tight")

            data = ('data:application/pdf;base64,' +
                    b64encode(pdf_io.getvalue()).decode("utf-8"))
            figures_data = {
                'data': data,
                'name': 'manufacturability.pdf',
                'mimetype': 'application/pdf'
            }
        else:
            figures_data = []
            for name, fig in figures:
                data = matplotlib_figure_to_svg_base64_data(
                    fig, bbox_inches="tight")
                figures_data.append({'img_data': data, 'name': name})

        return {
          'pdf_report': None if not PDF_REPORT else figures_data,
          'figures_data': None if PDF_REPORT else figures_data
        }

class EvaluateManufacturabilityView(StartJobView):
    serializer_class = serializer_class
    worker_class = worker_class
