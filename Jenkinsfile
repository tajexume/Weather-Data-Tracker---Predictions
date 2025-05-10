pipeline {
  agent any
  stages {
    stage('error') {
      steps {
        sh 'sh \'git https://github.com/tajexume/Weather-Data-Tracker---Predictions.git\''
      }
    }

    stage('Create VENV') {
      steps {
        sh ' sh \'ls || python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt\''
      }
    }

    stage('Run Script') {
      steps {
        sh 'sh \'source venv/bin/activate && python weather_cli currentWeather --city \\\'San Jose\\\'\''
      }
    }

  }
}