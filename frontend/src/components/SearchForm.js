import React, { Component } from 'react';
import styled from 'styled-components';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';

const SearchBar = styled.div`
display: flex;
justify-content: center;
margin-top:70px;   
`;
const SearchButton = styled.div`
display: flex;
justify-content: center;
    
`;
const useStyles = theme => ({
  root: {
    width: 340,
    margin: '3rem', 
  },
  media: {
    height: 140,
  },
});
class SearchForm extends Component {
  constructor(props){
    super(props);
    this.state={
      title:'',
      posts: []
    };
    this.onChange =this.onChange.bind(this);
    this.onSubmit =this.onSubmit.bind(this);
  }
  
  onChange(e){
    this.setState({
      [e.target.name]:e.target.value
    });
  }
  onSubmit(e){
    e.preventDefault();
    const post ={
      type:this.state.title
    }
/* 전송방식은 post */
    fetch('http://localhost:5000/search',{
      method :"POST",
      headers:{
        'content-type':'application/json'
      },
      body:JSON.stringify(post)
    })
    .then(res=>res.json())
    .then(data => this.setState({
        posts: data
    }));
  }
  render() {
    const { classes } = this.props;
    const {title, posts} = this.state;
    const postsList = posts.map((post) => (
        <div key={post.id} id={post.id}>
          
            <Card className={classes.root}>
      <CardActionArea>
        <CardMedia
          className={classes.media}
          image={post.image}
          title="Contemplative Reptile"
          height="100"
          width="100"
        />
        <CardContent>
          <Typography gutterBottom variant="h4" component="h3">
            {post.name} 
          </Typography>
          <Typography variant="body1" color="textSecondary" component="h3">
          필요한 기구: {post.tool} 
          </Typography>
        </CardContent>
      </CardActionArea>
      {/* <CardActions>
        <Button size="small" color="primary">
          Share
        </Button>
        <Button size="small" color="primary">
          Learn More
        </Button>
      </CardActions> */}
    </Card>

        </div>
    ));
    const {onChange,onSubmit} = this;
    return (
      <div>
        
    
        <form onSubmit={onSubmit}>
          <div>
          <SearchBar>
            <input type="text" name="title" value={title} onChange={onChange} 
            style={{ fontSize: "20px",border: '5px solid #B0F4E6',width: "30rem", height:"4rem"}}/>
            <button type="submit" style={{ border: '5px solid #B0F4E6', width: "5rem", height:"4rem",backgroundColor:"#B0F4E6",
           fontSize: "20px", color:"#FCF9EC"}}><text style={{color:"#12D3CF"}}>찾기</text></button>
            </SearchBar>
            <SearchButton>
            
            </SearchButton>
          </div>
        
          
        </form>
        <Box display="flex" flexWrap="wrap" justifyContent="center" m={10} p={3}>
       
                {postsList}
                </Box>
      </div>
    );
  }
}

export default withStyles(useStyles) (SearchForm);