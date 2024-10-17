// src/redux/modalSlice.js
import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  queryData: {},
  infData: {},
  // bodyText: "",
  isCreate: null,
  isPreview: false,
  currentFormData: null,
  openedDropdown: null,
  savedFormDataArr: [],
  stackedFormDataArr: [],
  createTopic: null,
  //currentPath in main-Slice use also here
};

const editSlice = createSlice({
  name: "data",
  initialState,
  reducers: {
    resetDataState: (state) => {
      state.infData = {};
      state.queryData = {};
    },
    openModal: (state) => {
      state.isOpen = true;
    },
    closeModal: (state) => {
      state.isOpen = false;
    },
    creating: (state) => {
      state.isCreate = true;
    },
    editing: (state) => {
      state.isCreate = false;
    },

    setImage: (state, action) => {
      state.selectedImage = action.payload;
    },
    clearImage: (state) => {
      state.selectedImage = null;
    },
    currentDropdown: (state, action) => {
      state.openedDropdown = action.payload;
    },
    //   clearEditState:(state)=>{

    //     isOpen: false,
    // selectedImage: null,
    // // bodyText: "",
    // isCreate: null,
    // isPreview: false,
    // currentFormData: null,
    // openedDropdown: null,
    //   },
    //   resetEditState: (state) =>{  openedDropdown: null,  selectedImage: null,

    //   },

    closeStackedArr: (state) => {
      const lastIndex = state.stackedFormDataArr.length - 1;
      if (lastIndex >= 0) {
        state.stackedFormDataArr[lastIndex] -= 1;
      }
    },
    openNewStack: (state, action) => {
      state.stackedFormDataArr = [...state.stackedFormDataArr, action.payload];
    },
    setCreateTopic: (state, action) => {
      state.createTopic = action.payload;
    },
  },
});

export const editAction = editSlice.actions;
export default editSlice;
