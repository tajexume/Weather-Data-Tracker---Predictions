pipeline {
  agent any
  stages {
    stage('Clone Repo') {
      steps {
        git(url: 'https://github.com/tajexume/Weather-Data-Tracker---Predictions.git', branch: 'main')
      }
    }

    stage('error') {
      steps {
        sh '''. .venv/Scripts/activate
pip install -r requirements.txt
python -m weather_cli --city \'San Jose\''''
      }
    }

  }
}