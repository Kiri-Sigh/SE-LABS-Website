import AboutDescription from "../../component/Description/About-Description/About-Description";
import RecentEvents from "../../component/Events/Recent-Events/Recent-Events";
import RecentNews from "../../component/News/Recent-News/Recent-News";
import TopicAndImage from "../../component/others/Big-Image/Topic-And-Image";
import { eventItems, newsItems } from "../../PlaceHolder-Data/data";
function AboutPage() {
  return (
    <>
      <TopicAndImage />
      <AboutDescription />
      <RecentNews newsItems={newsItems} />
      <RecentEvents eventItems={eventItems} />
    </>
  );
}
export default AboutPage;
