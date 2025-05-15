pipeline {
  agent any
  stages {
    stage('Clone Repo') {
      steps {
        git(url: 'https://github.com/tajexume/Weather-Data-Tracker---Predictions.git', branch: 'main')
      }
    }

    stage('Run Script') {
      steps {
        sh '''. .venv/Scripts/activate
pip install -r requirements.txt
python3 -m weather_cli.py current_weather --city \'San Jose\''''
      }
    }

  }
}