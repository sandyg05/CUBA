<template lang="pug">
.page
  h1  {{ infos.title }}
  web-links(:emailSubject="'[CUBA] Feedback on web app: ' + infos.title",
            tweetMessage="Optimize DNA sequences online",
            :tweetUrl="'http://cuba.genomefoundry.org/' + infos.path")
  img.icon.center-block(slot='title-img', :src='infos.icon')
  p.scenario-description Optimize a sequence with annotations representing constraints and objectives.

  learnmore(title='About this scenario')
    p Documentation in progress, come back later !



  .form
    h4.formlabel Provide an annotated sequence
    collapsible(title='Examples')
      file-example(filename='example_sequenc.gbk',
                   @input='function (e) {form.file = e}',
                   fileHref='/static/file_examples/sculpt_a_sequence/example_sequence.gbk',
                   imgSrc='/static/file_examples/sculpt_a_sequence/example_sequence_Map.svg')
        p.
          Collection of constructs assembled using random parts from the EMMA standard.
          Unzip the file and drag the genbank files into the file upload area.
    files-uploader(v-model='form.file', tip="Genbank/Snapgene format only",
                   :multiple='false')
    el-checkbox.animated.fadeIn(v-if='Object.keys(form.editedFeatures).length > 0',
                                v-model='form.editFeatures') Edit features
    featureseditor.animated.fadeIn(v-if='form.editedFeatures && form.editFeatures',
                      :sequence='form.sequence', v-model='form.editedFeatures',
                      :featureColor='editorFeatureColor')
    backend-querier(v-if='!validateForm().length',
                    :form='form', :backendUrl='infos.backendUrl',
                    :validateForm='validateForm', submitButtonText='Sculpt',
                    v-model='queryStatus')
    progress-bars(:bars='queryStatus.polling.data.bars', :order="['constraint', 'objective', 'location']"
                  v-if='queryStatus.polling.inProgress && queryStatus.polling.data')

  el-alert(v-if='queryStatus.requestError', :title="queryStatus.requestError",
     type="error", :closable="false")
  .results(v-if='!queryStatus.polling.inProgress')
    p.results-summary(v-if='queryStatus.result.summary',
                     v-html="queryStatus.result.summary")
    download-button(v-if='queryStatus.result.zip_file',
                    :filedata='queryStatus.result.zip_file')
  powered-by(:softwareNames='infos.poweredby')
</template>

<script>
import learnmore from '../../components/widgets/LearnMore'
import featureseditor from '../../components/widgets/FeaturesEditor/FeaturesEditor'

var bioparsers = require('bio-parsers')

var infos = {
  title: 'Sculpt a Sequence',
  navbarTitle: 'Sculpt a Sequence',
  path: 'sculpt_a_sequence',
  description: '',
  backendUrl: 'start/sculpt_a_sequence',
  icon: require('../../assets/images/sculpt_a_sequence.svg'),
  poweredby: ['dnachisel', 'dnafeaturesviewer']
}

export default {
  data () {
    return {
      form: {
        file: null,
        editFeatures: false,
        editedFeatures: {},
        sequence: ''
      },
      infos: infos,
      queryStatus: {
        polling: {},
        result: {},
        requestError: ''
      }
    }
  },
  components: {
    learnmore,
    featureseditor
  },
  infos: infos,
  methods: {
    handleSuccess (evt) {
      console.log(evt)
    },
    validateForm () {
      var errors = []
      if (!this.form.file) {
        errors.push('Provide at least one file.')
      }
      return errors
    },
    editorFeatureColor (feature) {
      var color = {
        '@': '#20a0ff',
        '~': '#ffd520'
      }[feature.label[0]]
      if (!color) {
        color = '#bed6e8'
      }
      return color
    }
  },
  watch: {
    'form.file.content' (value) {
      if (!value) {
        return
      }
      var genbank = atob(value.split(',')[1])
      this.form.editedFeatures = {}
      var self = this
      bioparsers.genbankToJson(genbank, function (result) {
        if (result.length === 1) {
          var parsed = result[0].parsedSequence
          self.form.sequence = parsed.sequence
          parsed.features.map(function (feature, id) {
            console.log(feature)
            self.$set(self.form.editedFeatures, id.toString(), {
              id: id.toString(),
              start: feature.start + 1,
              end: feature.end + 1,
              strand: feature.strand,
              label: feature.name,
              selected: false
            })
          })
        }
      })
    }
  }
}
</script>

<style scoped>

h4.formlabel {
  text-align: center;
  text-transform: uppercase;
  margin-top: 40px
}

.form {
  margin: 50px auto;
  max-width: 500px;
}

.title-img {
  height:80px;
  margin-top: -20px;
  margin-bottom: 20px;

}

.el-checkbox {
  font-weight: normal;
}


.el-select {
  width: 100%
}
</style>
