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
  // Using useQueries to handle multiple infinite queries in parallel
  const results = useQueries(
    urlArr.map((obj, i) => ({
      queryKey: ["infinite", obj.id, i], // Unique query key for each infinite query
      queryFn: ({ pageParam = 1 }) =>
        getData(`${obj.url}?page=${pageParam}&size=${obj.pageSize || 10}`), // Fetch with pagination
      getNextPageParam: (lastPage) => {
        // Determine next page based on data fetched
        return lastPage?.nextPage || undefined; // Example condition to determine if there are more pages
      },
      onSuccess: (data) => {
        return data;
      },
    }))
  );

  return results; // Return array of results
};
