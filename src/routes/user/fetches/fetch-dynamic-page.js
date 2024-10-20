import React, { useState } from "react";
import {
  //   useQueryClient,
  useMutation,
  useQuery,
  useQueries,
} from "@tanstack/react-query";
import { useParallelData, useInfiniteFetch } from "../../../api/custom-hooks";
import { useEffect } from "react";
// const fetchUrl = async (url) => {
//   const response = await fetch(url);
//   if (!response.ok) {
//     throw new Error("Network response was not ok");
//   }
//   return response.json();
// };

//whats needed
//users
//fetch initial -> id url
//fetch infinite q -> id url size page
//inf q take size and page and add to url
//admin
//create,

//state = fetcheddata={},isLoading=true,groupIdx=0
//parameter = groupList to fetch
//return = {{fetchedData={"id":data},isLoading=false/true}}

export const DataFetcherQueue = (template) => {
  //example fetchqueue = template
  const fetchQueue = [
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
    [
      {
        ID: "def",
        url: "https://jsonplaceholder.typicode.com/posts/3",
        type: "n",
      },
    ],
  ];
  //fetchedData= {{data:data},{data2:data2}}
  const [fetchedData, setFetchedData] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [currentGroupIndex, setCurrentGroupIndex] = useState(0);
  const [imageIDFetch, setImageIDFetch] = useState([]);
  const currentGroup = fetchQueue[currentGroupIndex];

  const normalQueries = currentGroup.filter((q) => q.type === "n");
  const infiniteQueries = currentGroup.filter((q) => q.type === "inf");

  const normalResults = useParallelData(normalQueries);

  const infiniteResults = useInfiniteFetch(infiniteQueries);

  const results = [...normalResults, ...infiniteResults];

  const allQueriesDone = results.every(
    (result) => result.isSuccess || result.isError
  );

  useEffect(() => {
    if (allQueriesDone && currentGroupIndex < fetchQueue.length - 1) {
      setFetchedData((prevData) => {
        const newData = results.reduce((acc, result, i) => {
          const uniqueKey = `${result.ID || result.queryKey[1]}-${i}`;

          if (result.data.pages) {
            acc[uniqueKey] = acc[uniqueKey]
              ? [...acc[uniqueKey], ...result.data.pages.flat()]
              : result.data.pages.flat();
          } else {
            acc[uniqueKey] = result.data;
          }
          return acc;
        }, {});

        return { ...prevData, ...newData }; // Merge new data with previous data
      });
      setCurrentGroupIndex((prev) => prev + 1); // Move to the next group
    } else if (allQueriesDone && currentGroupIndex === fetchQueue.length - 1) {
      // If last group is done, update loading state
      setIsLoading(false);
    }
  }, [allQueriesDone, currentGroupIndex, results, fetchQueue.length]);

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
