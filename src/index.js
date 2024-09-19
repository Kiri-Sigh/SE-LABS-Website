import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
// import { Provider } from "react-redux";
// import store from "./store/index.js";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import * as React from "react";
import * as ReactDOM from "react-dom/client";
import {
  ChakraBaseProvider,
  extendBaseTheme,
  theme as chakraTheme,
} from "@chakra-ui/react";

const { Button } = chakraTheme.components;

const theme = extendBaseTheme({
  components: {
    Button,
  },
});
const root = ReactDOM.createRoot(document.getElementById("root"));
const queryClient = new QueryClient();

root.render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      {/* <Provider store={store}> */}
      <ChakraBaseProvider theme={theme}>
        <App />
      </ChakraBaseProvider>
      {/* </Provider> */}
    </QueryClientProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
