import { createSlice } from "@reduxjs/toolkit";
const mainSlice = createSlice({
  name: "main",
  initialState: {
    items: [],
    currentPath: null,
    admin: false,
    researcher: false,
    leadResearcher: false,
  },
  reducers: {},
});
export default mainSlice;

//filter? bool (require filter in page or not)
//isEditing
//
