import React, { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import Table from "../components/Table";

const Statistics = () => {
    const useGetData = () => {
        const [ stat, setStat ] = useState([]);
        
        const getData = async () => {
            const getUrl = "http://localhost:5000/user/"
            await axios.get(getUrl)
            .then((response) => {
                if(response.data.error == "true"){
                    console.log("운동 기록 조회 에러");
                }
                else{
                    const allStat = [];
                    response.data.forEach(({ value }) => {
                        allStat.push(value);
                    });
                    setStat(allStat);
                }
            })
        }

        return {
            stat,
            getData,
        }
    }

    const { stat, getData } = useGetData();
    const columns = ["번호", "스쿼트", "푸시업", "운동 시간"];

    const getToday = () => {
        let today = new Date();
        let date = today.getDate();
        let month = today.getMonth() + 1;
        let year = today.getFullYear();

        return `${year}년 ${month}월 ${date}일`;
    }

    //번호, 스쿼트, 푸시업, 운동 시간
    const makeTable = () => {
        getData();
        return <Table today={getToday()}columns={columns} data={stat}/>
    }

    //총합 : 스쿼트 횟수, 푸시업 횟수, 총 운동 시간

    return(
        <div className="contents1">
            {makeTable()}
            <Link to='/'><button className="neutral middleBtn">돌아가기</button></Link>
        </div>
    )
}

export default Statistics;