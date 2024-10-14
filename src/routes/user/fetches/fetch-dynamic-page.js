import React, { useState } from "react";
import {
  //   useQueryClient,
  useMutation,
  useQuery,
  useQueries,
} from "@tanstack/react-query";
import { useParallelData } from "../../../api/custom-hooks";
import { useEffect } from "react";
// const fetchUrl = async (url) => {
//   const response = await fetch(url);
//   if (!response.ok) {
//     throw new Error("Network response was not ok");
//   }
//   return response.json();
// };

//[{},{}] =>
export const DataFetcherQueue = (template) => {
  // Queue with groups of URLs to fetch
  const fetchQueue = [
    //template here
    [
      { id: "abc", url: "https://jsonplaceholder.typicode.com/posts/1" },
      { id: "abc", url: "https://jsonplaceholder.typicode.com/posts/1" },
    ],
    [{ id: "abc", url: "https://jsonplaceholder.typicode.com/posts/1" }],
    [{ id: "abc", url: "https://jsonplaceholder.typicode.com/posts/1" }],
  ];
  const [fetchedData, setFetchedData] = useState({}); // Store fetched data
  const [isLoading, setIsLoading] = useState(true); // Track loading status
  const [currentGroupIndex, setCurrentGroupIndex] = useState(0);

  // Get the current group of URLs to fetch
  const currentGroup = fetchQueue[currentGroupIndex];

  // Use queries for the current group
  const results = useParallelData(fetchQueue[currentGroup]);

  // Check if all queries in the current group are successful
  const allQueriesDone = results.every(
    (result) => result.isSuccess || result.isError
  );
  // const anyLoading = results.some((result) => result.isLoading);

  React.useEffect(() => {
    if (allQueriesDone && currentGroupIndex < fetchQueue.length - 1) {
      setFetchedData((prevData) => {
        const newData = results.reduce((acc, result, i) => {
          const uniqueKey = `${result.queryKey[1]}-${i}`;
          acc[uniqueKey] = result; // Assuming 'id' is a unique identifier in each result
          return acc;
        }, {});

        return { ...prevData, ...newData }; // Merge new data with previous data
      });
      setCurrentGroupIndex((prev) => prev + 1); // Move to the next group
    } else if (allQueriesDone && currentGroupIndex === fetchQueue.length - 1) {
      // If it's the last group, update the loading state
      setIsLoading(false);
    }
  }, [allQueriesDone, currentGroupIndex, fetchQueue.length, results]);

  return { fetchedData, isLoading };
};

//////////////////check if all queries are done (parallel queries)
////////////////////////////////////////////////////////////////

// import { useQueries } from '@tanstack/react-query';

// const fetchPost = async (postId) => {
//   const response = await fetch(`/api/posts/${postId}`);
//   if (!response.ok) {
//     throw new Error('Network response was not ok');
//   }
//   return response.json();
// };

// const YourComponent = () => {
//   const postIds = [1, 2, 3]; // Example post IDs

//   const results = useQueries({
//     queries: postIds.map(postId => ({
//       queryKey: ['post', postId],
//       queryFn: () => fetchPost(postId),
//     })),
//   });

//   // Check if all queries are done
//   const allQueriesDone = results.every(result => result.isSuccess);

//   return (
//     <div>
//       {allQueriesDone ? (
//         results.map(result => <div key={result.data.id}>{result.data.title}</div>)
//       ) : (
//         <p>Loading...</p>
//       )}
//     </div>
//   );
// };
