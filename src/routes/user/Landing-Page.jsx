import React from "react";
import { Fragment } from "react";
import HeroBox from "../../component/others/Hero/Hero-box";
import { Button } from "@chakra-ui/react";
import RecentNews from "../../component/News/Recent-News";
function LandingPage() {
  return (
    <>
      <h1>Landing page</h1>
      <HeroBox />
      <RecentNews />
    </>
  );
}
export default LandingPage;
