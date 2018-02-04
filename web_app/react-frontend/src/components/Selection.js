import axios from 'axios'; 
import React, { Component } from 'react';
import AppService from './../services/AppService';
import { RingLoader } from 'react-spinners';

class Selection extends Component {
    
    constructor(props) {
        super(props);
        this.state = {
            selectedModel: 'ResNet50_deep',
            loading: false
        };
    }
    
    componentDidMount() {   
        this.appService = new AppService('http://127.0.0.1:8000/');
    }
    
    handleUploadFile(event) {
        this.setState({loading: true});
        
        this.appService.predictImage(this.state.selectedModel, event.target.files[0])
            .then(axios.spread((first, second) => {
                this.setState({loading: false});
                // console.log('handleUploadFile success:', first, second);
                this.props.onRetrieveData([first, second]);
            }))
            .catch((error) => {
                this.setState({loading: false});
                console.log(error);
            });
    }
    
    selectChange(event) {
        // console.log('selectChange:', event.target.value);
        this.setState({selectedModel: event.target.value});
    }
    
    render() {
        return (
            this.state.loading ? 
            <div>
                <div className="card app-card">
                    <div className="card-body">
                        <h5 className="card-title">Model Selection </h5>     
                        <div className="ring-loader-box">
                            <RingLoader className="loading-ring" color={'#3498db'} loading={this.state.loading} />
                        </div>
                    </div>
                 </div>
            </div>
            :
            <div>
                <div className="card app-card">
                    <div className="card-body">
                        <h5 className="card-title">Model Selection </h5>
            
                        <div className="form-section">
                            <form>
                                <div className="form-group">
                                    <label>Select One</label>
                                    <select className="form-control" value={this.state.selectedModel} onChange={this.selectChange.bind(this)}>
                                      <option value="ResNet50_deep">ResNet50_Deep (Best)</option>
                                      <option value="ResNet50_shallow">ResNet50_Shallow</option>
                                      <option value="original">Original Model</option>
                                      <option value="Xception">Xception</option>
                                    </select>
                                  </div>
                                      
                                <div className="form-group image-input">
                                    <div className="image-box">
                                        <label>Choose an image file</label>
                                        <input type="file" className="form-control-file" onChange={this.handleUploadFile.bind(this)}></input>
                                    </div>
                                </div>
                            </form>    
                        </div>
            
                    </div>
                </div>
            </div>
        );
    }
}

export default Selection;