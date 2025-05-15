pipeline {
  agent any
  stages {
    stage('Clone Repo') {
      parallel {
        stage('Clone Repo') {
          steps {
            git(url: 'https://github.com/tajexume/Weather-Data-Tracker---Predictions.git', branch: 'main')
          }
        }

        stage('error') {
          steps {
            sh 'cp "$weather_collector_secrets" .env'
          }
        }

      }
    }

    stage('Run Script') {
      steps {
        sh '''. .venv/Scripts/activate
pip install -r requirements.txt
python3 -m weather_cli currentweather --city \'San Jose\''''
      }
    }

  }
}