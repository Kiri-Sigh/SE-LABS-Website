import kmitl_logo from "../../../resource/kmitl_logo.webp";
const TopicAndImage = ({ data, image, isLoading, isLoading2 }) => {
  const firstKey = data?.[0] ? Object.keys(data[0])[0] : null;
  if (data) console.log("data", data); // Ensure data is logged
  const data2 = data ? data[0][firstKey].title : "";
  // if (data2) console.log("data2", data2); // Ensure data is logged
  const img = image ? image : kmitl_logo;

  return (
    <section className="flex overflow-hidden flex-col justify-center px-16 py-28 w-full bg-sky-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
      <div className="flex flex-col w-full max-md:max-w-full">
        <h1 className="overflow-hidden w-full text-5xl font-bold leading-tight text-black max-md:max-w-full max-md:text-4xl">
          {isLoading ? "loading..." : data2} {/* Dynamically show title */}
        </h1>
        <div className="flex flex-col mt-20 w-full max-md:mt-10 max-md:max-w-full">
          <img
            loading="lazy"
            src={isLoading2 ? kmitl_logo : img}
            alt="AI Laboratory visual representation"
            className="object-contain w-full aspect-[2.19] max-md:max-w-full"
          />
        </div>
      </div>
    </section>
  );
};
export default TopicAndImage;
