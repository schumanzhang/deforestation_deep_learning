import axios from 'axios'; 

class AppService {
    
    constructor(url) {
        this.baseUrl = url;
    }
    
    getOriginal(url) {
        return axios.get(url + 'deforestation_app/api/original');
    }
    
    getResNet50Shallow(url) {
        return axios.get(url + 'deforestation_app/api/resnet-shallow');
    }
    
    getResNet50Deep(url) {
        return axios.get(url + 'deforestation_app/api/resnet-deep');
    }
    
    getXception(url) {
        return axios.get(url + 'deforestation_app/api/xception');
    }
    
    makePrediction(selectedModel, fileData) {
        const formData = new FormData();
        formData.append('modelName', selectedModel);
        formData.append('image', fileData, { type: 'image/jpg' });
        formData.append('imageName', fileData.name);
        
        return axios({
          url: this.baseUrl + 'deforestation_app/api/predict-image',
          method: 'POST',
          data: formData,
          headers: {
            Accept: 'application/json',
            'Content-Type': 'multipart/form-data'
          }
        });
    }
    
    predictImage(selectedModel, fileData) {
        
        let predictionModel;
        
        switch(selectedModel) {
            case 'ResNet50_deep':
                predictionModel = this.getResNet50Deep;
                break;
            case 'ResNet50_shallow':
                predictionModel = this.getResNet50Shallow;
                break;
            case 'original':
                predictionModel = this.getOriginal;
                break;
            case 'Xception':
                predictionModel = this.getXception;
                break;
            default:
                predictionModel = this.getResNet50Deep;

        }
        console.log('predictImage:', fileData.name);
        return axios.all([predictionModel(this.baseUrl), this.makePrediction(selectedModel, fileData)])
    }
    
}

export default AppService