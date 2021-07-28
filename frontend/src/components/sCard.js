import React, { useState, useRef, useEffect }  from "react";
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

const Styles = makeStyles({
    root: {
      maxWidth: 345,
    },
    media: {
      height: 140,
    },
  });

const sCard = ({ data }) => {
    const classes = Styles();
    var ex_name = []
    var ex_tool = []
    var ex_image = []

    data.map(value => {
      ex_name.push(value.ex_name);
      ex_image.push(value.ex_image);
      ex_tool.push(value.ex_tool);
        console.log("fsssiusluvbuawvorubaivwblrbwbuubuw");
        console.log(ex_name);
        console.log(ex_image);
        console.log(ex_tool);
    })

    return(
        <div>
       {ex_name}
       {ex_tool}
       {ex_image}
                    </div>
    );
}

export default sCard;