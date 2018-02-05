import React, { Component } from 'react';

class Details extends Component {
    
    constructor(props) {
        super(props);
        this.state = {
            hasInfo: false,   
            imageLink: '',
            prediction: ''
        };
    }
    
    componentWillReceiveProps = (nextProps) => {
        console.log('componentWillReceiveProps:', nextProps)
        this.setState({hasInfo: true});
        this.setState({imageLink: 'http://127.0.0.1:8000/' + nextProps.hasData[1].data.Location});
        this.setState({prediction: ' ' + nextProps.hasData[1].data.prediction.join(',')});
    }
    
    render() {
        return (
            this.state.hasInfo ?
            <div>
                <div className="card app-card-right">
                    <div className="card-body">
                        <h5 className="card-title">Details</h5>
                        <p> The chosen model has the following scores </p>
                        
                        <strong> Recall score: </strong>
                        <span>{this.props.hasData[0].data.Recall_score}</span>
                        <br/>
                        <strong> Precision score: </strong>
                        <span>{this.props.hasData[0].data.Precision_score}</span>
                        <br/>
                        <strong> F-beta score: </strong>
                        <span>{this.props.hasData[0].data.Fbeta_score}</span>
            
                        <div className="show-image-box">
                            <img className="display-image" src={this.state.imageLink}/>
                        </div>
                        <br/>
                        <p>
                            <strong>Prediction:</strong> 
                            {this.state.prediction}
                        </p>
                    </div>
                </div>
            </div>
            :
            <div>
                <div className="card app-card-right">
                    <div className="card-body">
                        <h5 className="card-title">Details</h5>
                        
                        <p> Please upload a satellite image of the Amazon rainforest... </p>
                    </div>
                </div>
            </div>
        );
    }
}

export default Details;