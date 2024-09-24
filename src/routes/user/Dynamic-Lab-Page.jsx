import Description from "../../component/Description/Description";
import RecentEvents from "../../component/Events/Recent-Events/Recent-Events";
import RecentNews from "../../component/News/Recent-News/Recent-News";
import TopicAndImage from "../../component/others/Big-Image/Topic-And-Image";
import RecentPublications from "../../component/Publications/Recent-Publications";
import RecentResearch from "../../component/Research/Recent-Research";
import OurTeam from "../../component/Team/Our-Team";
import {
  eventItems,
  newsItems,
  teamMembers,
  researchItems,
  publicationItems,
} from "../../PlaceHolder-Data/data";

function DynamicLabPage() {
  return (
    <>
      <TopicAndImage />
      <Description />
      <OurTeam teamMembers={teamMembers} />
      <RecentResearch researchItems={researchItems} />
      <RecentNews newsItems={newsItems} />
      <RecentPublications publicationItems={publicationItems} />
      <RecentEvents eventItems={eventItems} />
    </>
  );
}
export default DynamicLabPage;

//fetch lab info, fetch image, then fetch projects etc...
