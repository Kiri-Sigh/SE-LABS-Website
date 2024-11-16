import {
  useQueries,
  useInfiniteQuery,
  // useMutation,
  useQuery,
} from "@tanstack/react-query";
import { getData, getImgData } from "./api-method";
// import { useState } from "react";
//   //map [{url,id},{}] to {id:{data},id:{data}}
//   //using getData each of the obejects in array
//   //and using useQueries
export const useNormalQueryGet = (url, type, id = "") => {
  const results = useQuery({
    queryKey: [`get-${type}-${id}`],
    queryFn: () => getData(url),
    onSuccess: (data) => {
      return data;
    },
  });

  return results;
};
export const useQueryGetImg = (url, type, id) => {
  const results = useQuery({
    queryKey: [`get-${type}-${id}`],
    staleTime: 1000 * 60, // Data stays fresh for 1 minute
    cacheTime: 1000 * 60 * 5, // Cache remains for 5 minutes

    queryFn: () => {
      const type2 = type.toLowerCase();
      return getImgData(`${url}/${type2}/image-high?${type2}_id=${id}`);
    },
    // enabled: relatedTopic !== null, // Only run query if data is not null
    onSuccess: (data) => {
      console.log("fetched img", url, type);
      return data;
    },
  });

  return results;
};

export const useParallelData = (urlArr) => {
  const results = useQueries(
    urlArr.map((obj, i) => ({
      queryKey: [`${"get-" + obj.id + "-" + i}`],
      queryFn: () => getData(obj.url),
      onSuccess: (data) => {
        console.log("fetched par data", urlArr[1]);

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
export const useInfiniteFetch = (obj) => {
  const result = useInfiniteQuery({
    queryKey: [
      `infinite-${obj.id}-${obj.pageSize}`,
      JSON.stringify(obj.filter),
    ],
    // Include filter in key
    queryFn: ({ pageParam = 1 }) => {
      let url = obj.url;

      // Handle query params dynamically
      const params = new URLSearchParams();
      params.append("page", pageParam);
      params.append("amount", obj.pageSize);

      if (obj.filter) {
        Object.entries(obj.filter).forEach(([key, value]) => {
          params.append(key, value);
        });
      }

      // Append serialized params to the URL
      if (url.slice(-1) === "?") {
        url += params.toString();
      } else {
        url += `&${params.toString()}`;
      }

      console.log("Fetching URL:", url); // Debugging URL
      return getData(url); // Perform the fetch
    },
    getNextPageParam: (lastPage, allPages) => {
      // Adjust based on your API's response structure
      // console.log("lastpage=", lastPage);
      // console.log("alloage=", allPages);
      const dataLength = lastPage?.length || 0;
      if (dataLength < obj.pageSize) {
        // console.log("data;ennght", dataLength);
        // console.log("no more page");
        return undefined;
      } // No more pages
      return allPages.length + 1; // Increment page
    },
    enabled: true, // Ensure it's enabled
    refetchOnWindowFocus: false, // Avoid refetch on tab switch
    onSuccess: (data) => console.log("Fetched data:", data),
    onError: (error) => console.error("Error fetching data:", error),
  });

  // console.log("Infinite Query Result:", result);
  return result; // Return the infinite query result
};
export const useInfiniteFetchFilter = (obj) => {
  const result = useInfiniteQuery({
    queryKey: [
      `infinite-${obj.id}-${obj.pageSize}`,
      JSON.stringify(obj.filter),
    ],
    // Include filter in key
    queryFn: ({ pageParam = 1 }) => {
      let url = obj.url;
      // Handle query params dynamically
      const params = new URLSearchParams();
      params.append("page", pageParam);
      params.append("amount", obj.pageSize);

      if (obj.filter) {
        Object.entries(obj.filter).forEach(([key, value]) => {
          params.append(key, value);
        });
      }

      // Append serialized params to the URL
      if (url.slice(-1) === "?") {
        url += params.toString();
      } else {
        url += `&${params.toString()}`;
      }

      console.log("Fetching URL:", url); // Debugging URL
      return getData(url); // Perform the fetch
    },
    getNextPageParam: (lastPage, allPages) => {
      // Adjust based on your API's response structure
      // console.log("lastpage=", lastPage);
      // console.log("alloage=", allPages);
      const dataLength = lastPage?.length || 0;
      if (dataLength < obj.pageSize) {
        // console.log("data;ennght", dataLength);
        // console.log("no more page");
        return undefined;
      } // No more pages
      return allPages.length + 1; // Increment page
    },
    enabled: true, // Ensure it's enabled
    refetchOnWindowFocus: false, // Avoid refetch on tab switch
    onSuccess: (data) => console.log("Fetched data:", data),
    onError: (error) => console.error("Error fetching data:", error),
  });

  // console.log("Infinite Query Result:", result);
  return result; // Return the infinite query result
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
