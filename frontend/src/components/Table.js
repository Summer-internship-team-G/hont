import React from "react";

const Table = ({ today, columns, data }) => {
    let num = 1;
    let squatSum = 0;
    let pushupSum = 0;
    let timeSum = 0;

    data.map(value => {
        squatSum += Number(value.squatNum);
        pushupSum += Number(value.pushupNum);
        timeSum += Number(value.exerTime);
    })

    return(
        <table>
            <caption className="textShadow2">{today}</caption>
            <thead>
                <tr>
                    {columns.map((column) => (
                        <th key={column}>{column}</th>
                    ))}
                </tr>
            </thead>
            <tbody>
                {data.map(value => (
                    <tr key = {num + value.squatNum + value.pushupNum + value.exerTime}>
                        <td>{num++}</td>
                        <td>{Number(value.squatNum)}회</td>
                        <td>{Number(value.pushupNum)}회</td>
                        <td>{Number(value.exerTime)}초</td>
                    </tr>
                ))}
                {/* {data.map(({ squat, pushup, time }) => (
                    <tr key={ num + squat + pushup + time}>
                        <td>{num++}</td>
                        <td>{Number(squat)}회</td>
                        <td>{Number(pushup)}회</td>
                        <td>{Number(time)}초</td>
                    </tr>
                ))} */}
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