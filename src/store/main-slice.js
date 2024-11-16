import { createSlice } from "@reduxjs/toolkit";
const mainSlice = createSlice({
  name: "main",
  initialState: {
    items: [], //after login user data
    currentPath: null,
    admin: true,
    researcher: false,
    leadResearcher: false,
    itemQuantity: null,
    token: null,
    labData: null,
    fetchedLabData: false,
  },
  reducers: {
    isAdmin: (state) => {
      state.admin = true;
      state.researcher = false;
      state.leadResearcher = false;
    },
    isLead: (state) => {
      state.admin = false;
      state.researcher = false;
      state.leadResearcher = true;
    },
    isResearcher: (state) => {
      state.admin = false;
      state.researcher = true;
      state.leadResearcher = false;
    },
    boolFetchLabData: (state) => {
      state.fetchedLabData = true;
    },
    setLabData: (state, action) => {
      state.labData = action.payload;
    },
  },
});
export const mainAction = mainSlice.actions;

export default mainSlice;

//filter? bool (require filter in page or not)
//isEditing
//
