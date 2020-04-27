import React, { Component } from 'react';
import LabelingApp from './LabelingApp';

import { Loader } from 'semantic-ui-react';
import DocumentMeta from 'react-document-meta';

import { demoMocks } from './demo';

export default class LabelingLoader extends Component {
  constructor(props) {
    super(props);
    this.state = {
      project: null,
      image: null,
      isLoaded: false,
      error: null,
    };
  }

  async fetch(...args) {
    const { projectId } = this.props.match.params;
    if (projectId === 'demo') {
      const path = typeof args[0] === 'string' ? args[0] : args[0].pathname;
      return demoMocks[path](...args);
    }

    return await fetch(...args);
  }

  componentDidMount() {
    this.refetch();
  }

  componentDidUpdate(prevProps) {
    if (prevProps.match.params.imageId !== this.props.match.params.imageId) {
      this.refetch();
    }
  }

  async refetch() {
    this.setState({
      isLoaded: false,
      error: null,
      project: null,
      image: null,
    });

    const { match, history } = this.props;
    const { projectId, imageId } = match.params;
    
    try {
      // const a = document.createElement('a');
      // a.setAttribute('href', 'http://localhost:8000/getLabelingInfo/1/1');
      // const url = new URL(a.href);
      // url.searchParams.append('projectId', projectId);
      // if (imageId) {
      //   url.searchParams.append('imageId', imageId);
      // }
      // const { project, image } = await (await this.fetch('http://localhost:8000/getLabelingInfo/1/1')).json();
      // console.log(project, image);
      
      // console.log(project, image);
      const project = await (await this.fetch(
        `http://localhost:8000/projects/1/`
      )).json();
      const image1 = await (await this.fetch(
        `http://localhost:8000/images/1/`
      )).json();
      
      const forms = project.forms;
      const dict = {};
      forms.forEach(element => {
        dict[element.id] = [];
      });
      image1.imageFigures.forEach(element=>{
        dict[element.formId].push({
          id:element.id,
          type: element.type,
          points: element.points,
          tracingOptions: element.tracingOptions
        })
      });
    
      const image = {
        id: image1.id,
        lastEdited: 12313,
        projectsId: project.name,
        originalName: image1.originalName,
        link: image1.link,
        externalLink: null,
        localPath: null,
        labeled: 0,
        labelData: {
          labels: dict,
          },
        };
        console.log(image)
      // console.log(1);
      // console.log(2);
      if (!project) {
        history.replace(`/label/${projectId}/over`);
        return;
      }

      history.replace(`/label/${project.id}/${image.id}`);
      // history.replace(`/label/${project.id}/${image.id}`);


      this.setState({
        isLoaded: true,
        project,
        image,
      });
    } catch (error) {
      this.setState({
        isLoaded: true,
        error,
      });
    }
  }

  async pushUpdate(labelData) {
    const { imageId } = this.props.match.params;
    await this.fetch('/api/images/' + imageId, {
      method: 'PATCH',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ labelData }),
    });
  }

  async markComplete() {
    const { imageId } = this.props.match.params;
    await this.fetch('http://localhost:8000/images/' + imageId, {
      method: 'PATCH',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ labeled: true }),
    });
  }

  render() {
    const { history } = this.props;
    const { project, image, isLoaded, error } = this.state;

    if (error) {
      return <div>Error: {error.message}</div>;
    } else if (!isLoaded) {
      return <Loader active inline="centered" />;
    }

    const title = `Image ${image.id} for project ${project.name} -- Label Tool`;

    const props = {
      onBack: () => {
        history.goBack();
      },
      onSkip: () => {
        history.push(`/label/${project.id}/`);
      },
      onSubmit: () => {
        this.markComplete();
        history.push(`/label/${project.id}/`);
      },
      onLabelChange: this.pushUpdate.bind(this),
    };

    const { referenceLink, referenceText } = project;

    return (
      <DocumentMeta title={title}>
        <LabelingApp
          labels={project.forms}
          reference={{ referenceLink, referenceText }}
          labelData={image.labelData.labels || {}}
          // labelData={image.imageFigures || {}}

          imageUrl={image.link}
          fetch={this.fetch.bind(this)}
          demo={project.id === 'demo'}
          {...props}
        />
      </DocumentMeta>
    // <h1> {this.state.project.forms[0]}  </h1>
    
    );
  }
}
