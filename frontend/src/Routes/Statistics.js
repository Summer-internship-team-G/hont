import React, { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import Table from "../components/Table";

const Statistics = () => {
    const useGetData = () => {
        const [ stat, setStat ] = useState([]);

        const postData = async () => {
            const postUrl = "http://localhost:5000/exercise/statistics"
            const postVal = {
                id: localStorage.getItem('id'),
                exerDate: `${year}. ${month}. ${date}.`,
            }
            await axios.post(postUrl, postVal, {
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then((response) => {
                if(response.data.error){
                    console.log("운동 기록 조회 에러");
                }
                else{
                    const allStat = [];
                    response.data['key'].map(value => {
                        allStat.push(value);
                    });
                    // response.data['key'].forEach(({ value }) => {
                    //         allStat.push(value);
                    // });
                    setStat(allStat);
                    console.log("---------");
                    console.log(stat);
                }
            })
        }

        
        //번호, 스쿼트, 푸시업, 운동 시간
        // const makeTable = () => {
        //     postData();
        //     return <Table today={getToday()} columns={columns} data={stat}/>
        // }
        
        return {
            postData,
            stat,
        }
    }
    
    const { postData, stat } = useGetData();
    const columns = ["번호", "스쿼트", "푸시업", "운동 시간"];
    
    const newDate = new Date();
    const date = newDate.getDate();
    const month = newDate.getMonth() + 1;
    const year = newDate.getFullYear();
    const today = `${year}년 ${month}월 ${date}일`;

    postData();
    //총합 : 스쿼트 횟수, 푸시업 횟수, 총 운동 시간

    return(
        <div className="contents1">
            <Table today={today} columns={columns} data={stat}/>
            <Link to='/'><button className="neutral middleBtn boxShadow">돌아가기</button></Link>
        </div>
    )
}

export default Statistics;