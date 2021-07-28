import React, { Component } from 'react';

class SearchItem extends Component {
    /* 컴포넌트 생성시 */
    /* 생명주기순서 : constructor(생성자) -> componentWillMount -> render */
    constructor(props) {
        super(props);
        this.state = {
            posts: []
        }
    }
    componentWillMount() {
        fetch('http://localhost:5000/search')
            .then(res => res.json())
            .then(data => this.setState({
                posts: data
            }));
            
    }
    render() {
        const { posts } = this.state;
        const postsList = posts.map((post) => (
            <div key={post.id} id={post.id}>
                <h4>{post.name}</h4>
                <h4>{post.tool}</h4>
            </div>
        ));
        return (
            <div>
                {postsList}
            </div>
        );
    }
}
export default SearchItem;