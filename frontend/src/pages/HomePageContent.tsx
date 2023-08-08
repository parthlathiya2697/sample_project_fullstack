import React, { useState, useEffect } from "react";
import axios from "axios";
import { DUMMY_BASE_URL } from '../generated/common';

const CompletedUsersCount = () => {
  const [completedUsersCount, setCompletedUsersCount] = useState(null);
  const [averageDuration, setAverageDuration] = useState(null);
  const [totalsData, setTotalsData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(DUMMY_BASE_URL + "/api/v1/items/completed-count");
        setCompletedUsersCount(response.data);

        const averageResponse = await axios.get(DUMMY_BASE_URL + "/api/v1/items/average_per_user");
        setAverageDuration(averageResponse.data.average_per_user); // Extract the relevant value

        const totalsResponse = await axios.get(DUMMY_BASE_URL + "/api/v1/items/average_duration_completed");
        setTotalsData(totalsResponse.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      {completedUsersCount !== null ? (
        <p>Completed Users Count: {completedUsersCount}</p>
      ) : (
        <p>Loading...</p>
      )}
      
      {averageDuration !== null ? (
        <p>Average Duration: {averageDuration}</p>
      ) : (
        <p>Loading...</p>
      )}
      
      {totalsData !== null ? (
       <p>Average Duration Completed: {totalsData}</p>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default CompletedUsersCount;
