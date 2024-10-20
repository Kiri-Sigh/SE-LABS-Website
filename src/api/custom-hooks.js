import {
  useQueries,
  useInfiniteQuery,
  // useMutation,
  // useQuery,
} from "@tanstack/react-query";
import { getData } from "./api-method";
// import { useState } from "react";
//   //map [{url,id},{}] to {id:{data},id:{data}}
//   //using getData each of the obejects in array
//   //and using useQueries
export const useParallelData = (urlArr) => {
  const results = useQueries(
    urlArr.map((obj, i) => ({
      queryKey: [`${"get-" + obj.id + "-" + i}`],
      queryFn: () => getData(obj.url),
      onSuccess: (data) => {
        return data;
      },
      //   onSettled:
    }))
  );

  return results;
};

// [
//   {
//     queryKey: ["get", "1", 0],
//     isLoading: false,
//     isSuccess: true,
//     data: {
//       id: 1,
//       title: "Post 1",
//       body: "This is the body of post 1."
//     },
//     error: null,
//   },
//   {
//     queryKey: ["get", "2", 1],
//     isLoading: false,
//     isSuccess: true,
//     data: {
//       id: 2,
//       title: "Post 2",
//       body: "This is the body of post 2."
//     },
//     error: null,
//   }
// ];

// Hook for handling a single infinite fetch query
export const useInfiniteFetch = ({ obj }) => {
  const result = useInfiniteQuery(
    [`${"infinite-" + obj.id}`], //
    ({ pageParam = 1 }) =>
      getData(`${obj.url}?page=${pageParam}&size=${obj.pageSize}`),
    {
      getNextPageParam: (lastPage, allPages) => {
        const dataLength = lastPage?.data?.length || 0;

        // If data length is less than pageSize, no more pages
        if (dataLength < obj.pageSize) {
          return undefined;
        }

        // Otherwise, return the next page number
        return allPages.length + 1;
      },
      onSuccess: (data) => {
        console.log("Fetched data:", data);
      },
    }
  );

  return result; // Return the result from the infinite query
};
// {
//   data: {
//     pages: [
//       [
//         { id: 1, title: "Post 1", body: "This is post 1 body." },
//         { id: 2, title: "Post 2", body: "This is post 2 body." },
//         // 3 more posts here (page size 5)
//       ],
//       [
//         { id: 6, title: "Post 6", body: "This is post 6 body." },
//         { id: 7, title: "Post 7", body: "This is post 7 body." },
//         // 3 more posts here (page size 5)
//       ]
//     ]
//   },
//   isFetchingNextPage: false,
//   hasNextPage: true,
//   fetchNextPage: () => {/* Function to fetch the next page */},
//   isSuccess: true,
//   error: null,
// }
