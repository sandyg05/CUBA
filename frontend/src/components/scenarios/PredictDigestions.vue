<template lang="pug">

.page
  h1 Digestion Pattern Predictor
  web-links(:emailSubject="'[CUBA] Feedback on web app: ' + infos.title",
            tweetMessage="Online restriction digest simulator:",
            :tweetUrl="'http://cuba.genomefoundry.org/' + infos.path")
  img.icon.center-block(slot='title-img', :src='infos.icon')
  p.scenario-description Submit sequences and an enzymatic mixes, get migration predictions.


  .form
    h4.formlabel Ladder
    ladderselector(v-model='form.ladder')

    h4.formlabel Digestions
    digestionset(v-model='form.digestions')
    h4.formlabel Sequences
    sequencesuploader(v-model='form.files')
    p
      el-checkbox(v-model='form.makeReport') Generate report
    p
      el-checkbox(v-model='form.showBandsSizes') Show band sizes in plot.
    backend-querier(:form='form', :backendUrl='infos.backendUrl',
                    :validateForm='validateForm', submitButtonText='Predict patterns',
                    v-model='queryStatus')
    el-alert(v-if='queryStatus.requestError', :title="queryStatus.requestError",
       type="error", :closable="false")
    .results(v-if='!queryStatus.polling.inProgress')
      download-button(v-if='queryStatus.result.file',
                      :filedata='queryStatus.result.file')
      .results-summary(v-if='queryStatus.result.preview',
                       v-html="queryStatus.result.preview.html")
  powered-by(:softwareNames='infos.poweredby')
</template>

<script>
import learnmore from '../../components/widgets/LearnMore'
import sequencesuploader from '../../components/widgets/SequencesUploader'
import digestionset from '../../components/widgets/DigestionSelectorSet'
import ladderselector from '../../components/widgets/LadderSelector'

var infos = {
  title: 'Predict Digestions',
  navbarTitle: 'Predict Digestions',
  path: 'predict-digestions',
  description: '',
  backendUrl: 'start/predict_digestions',
  icon: require('../../assets/images/predict-icon.svg'),
  poweredby: ['bandwagon']
}

export default {
  data () {
    return {
      form: {
        ladder: '100_to_4k',
        digestions: [],
        makeReport: false,
        files: [],
        showBandsSizes: false
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
    sequencesuploader,
    learnmore,
    digestionset,
    ladderselector
  },
  infos: infos,
  methods: {
    handleSuccess (evt) {
      console.log(evt)
    },
    validateForm () {
      var errors = []
      if (this.form.digestions.length === 0) {
        errors.push('Provide at least one digestion')
      }
      if (this.form.files.length === 0) {
        errors.push('Provide at least one sequence file')
      }
      return errors
    }
  }
}
</script>

<style lang='css' scoped>

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
