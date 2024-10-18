import {
  useQueries,
  useInfiniteQuery,
  useMutation,
  useQuery,
} from "@tanstack/react-query";
import { getData } from "./api-method";
import { useState } from "react";
//   //map [{url,id},{}] to {id:{data},id:{data}}
//   //using getData each of the obejects in array
//   //and using useQueries
export const useParallelData = (urlArr) => {
  const results = useQueries(
    urlArr.map((obj, i) => ({
      queryKey: ["get", obj.id, i],
      queryFn: () => getData(obj.url),
      onSuccess: (data) => {
        return data;
      },
      //   onSettled:
    }))
  );

  return results;
};
// hooks/useInfiniteFetch.js

export const useInfiniteFetch = (urlArr) => {
  const results = useQueries(
    urlArr.map((obj, i) => ({
      queryKey: ["infinite", obj.id, i], // Unique query key for each infinite query
      queryFn: ({ pageParam = 1 }) =>
        getData(`${obj.url}?page=${pageParam}&size=${obj.pageSize || 10}`), // Fetch with pagination
      getNextPageParam: (lastPage, allPages) => {
        // Extract the relevant data and compare the length to the pageSize
        const pageSize = obj.pageSize || 10;
        const dataLength = lastPage?.data?.length || 0; // Assuming data is in `lastPage.data`

        // If data length is less than pageSize, no more pages, return undefined
        if (dataLength < pageSize) {
          return undefined;
        }

        // Otherwise, return the next page
        return allPages.length + 1; // Assuming simple page increment logic
      },
      onSuccess: (data) => {
        return data;
      },
    }))
  );

  return results; // Return array of results
};
