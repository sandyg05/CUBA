<template lang="pug">

.page
  h1  {{ infos.title }}
  web-links(:emailSubject="'[CUBA] Feedback on web app: ' + infos.title",
            tweetMessage="Convert sequences formats to Genbank or Fasta",
            :tweetUrl="'http://cuba.genomefoundry.org/' + infos.path")
  img.icon.center-block(slot='title-img', :src='infos.icon')


  .form

    h4.formlabel Sequence(s) to convert
    files-uploader(v-model='form.files', :multiple='true',
                   tip="Accepted formats: Genbank/Fasta/Snapgene/MSDoc")

    h4.formlabel Desired format
    .report-radio
      el-radio(v-model='form.format', class="radio", label='genbank') Genbank
      el-radio(v-model='form.format', class="radio", label='fasta') Fasta
    .checkbox
      el-checkbox(v-if="form.format === 'fasta'"
                  v-model='form.inSingleFile') All sequences in a single file


    backend-querier(:form='form', :backendUrl='infos.backendUrl',
                    :validateForm='validateForm', submitButtonText='Evaluate',
                    v-model='queryStatus')
    el-alert(v-if='queryStatus.requestError', :title="queryStatus.requestError",
       type="error", :closable="false")
    .results(v-if='!queryStatus.polling.inProgress')
      download-button(v-if='queryStatus.result.file',
                      :filedata='queryStatus.result.file')
  powered-by(:softwareNames='infos.poweredby')
</template>

<script>
// import filesuploader from '../../components/widgets/FilesUploader'

var infos = {
  title: 'Convert Sequence Files',
  navbarTitle: 'Convert Sequence Files',
  path: 'convert_sequence_files',
  description: '',
  backendUrl: 'start/convert_sequence_files',
  icon: require('../../assets/images/convert_sequence_files.svg'),
  poweredby: ['crazydoc']
}

export default {
  data () {
    return {
      enzymes: ['BsaI', 'BsmBI', 'BbsI'],
      form: {
        format: 'genbank',
        inSingleFile: false,
        files: []
      },
      infos: infos,
      ladder_options: [
        {
          label: 'Ladder 100 bp - 4000 bp',
          value: '100-4k'
        }
      ],
      queryStatus: {
        polling: {},
        result: {},
        requestError: ''
      }
    }
  },
  infos: infos,
  methods: {
    handleSuccess (evt) {
      console.log(evt)
    },
    validateForm () {
      var errors = []
      if (this.form.files.length === 0) {
        errors.push('Provide at least one sequence.')
      }
      return errors
    }
  }
}
</script>

<style lang='scss' scoped>

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

.report-radio {
  text-align: center;
  margin: 0 auto;
  .el-radio {
    margin-bottom: 20px;
  }
}

.checkbox {
  text-align: center;
}

.files-number p {
  margin-top: -10px;
  font-size: 0.8em;
}

.figure-preview {
  margin-bottom: 5em;
  img {
    width:100%;
  }
}
</style>
