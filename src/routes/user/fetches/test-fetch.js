import React from "react";
import { DataFetcherQueue } from "./DataFetcherQueue";

const App = () => {
  const fetchQueueA = [
    [
      {
        ID: "abc",
        url: "https://jsonplaceholder.typicode.com/posts/1",
        type: "inf",
        pageSize: 5,
      },
      {
        ID: "xyz",
        url: "https://jsonplaceholder.typicode.com/posts/2",
        type: "n",
      },
    ],
  ];

  const fetchQueueB = [
    [
      {
        ID: "def",
        url: "https://jsonplaceholder.typicode.com/posts/3",
        type: "n",
      },
    ],
  ];

  // Fetch data from both queues
  const { fetchedData: dataA, isLoading: loadingA } =
    DataFetcherQueue(fetchQueueA);
  const { fetchedData: dataB, isLoading: loadingB } =
    DataFetcherQueue(fetchQueueB);

  // Combine loading state
  const isLoading = loadingA || loadingB;

  return (
    <div>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <>
          <h1>Fetched Data A:</h1>
          <pre>{JSON.stringify(dataA, null, 2)}</pre>

          <h1>Fetched Data B:</h1>
          <pre>{JSON.stringify(dataB, null, 2)}</pre>
        </>
      )}
    </div>
  );
};

export default App;
