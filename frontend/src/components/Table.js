import React from "react";

const Table = ({ today, columns, data }) => {
    let num = 1;
    let squatSum = 0;
    let pushupSum = 0;
    let timeSum = 0;

    data.map(({squat, pushup, time}) =>{
        squatSum += squat;
        pushupSum += pushup;
        timeSum += time;
    });

    return(
        <table>
            <caption>{today}</caption>
            <thead>
                <tr>
                    {columns.map((column) => (
                        <th key={column}>{column}</th>
                    ))}
                </tr>
            </thead>
            <tbody>
                {data.map(({ squat, pushup, time }) => (
                    <tr key={ num + squat + pushup + time}>
                        <td>{num++}</td>
                        <td>{squat}회</td>
                        <td>{pushup}회</td>
                        <td>{time}초</td>
                    </tr>
                ))}
                <tr key="합계">
                    <td>합계</td>
                    <td>{squatSum}회</td>
                    <td>{pushupSum}회</td>
                    <td>{timeSum}초</td>
                </tr>
            </tbody>
        </table>
    );
}

export default Table;