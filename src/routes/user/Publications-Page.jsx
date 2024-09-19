import React from 'react';
import Header from '../../component/Header.jsx/Header';
import PublicationCard from '../../component/Recent-Publications';
import Footer from '../../component/Footer/footer';
const publicationsData = [
  {
    image: "https://cdn.builder.io/api/v1/image/assets/TEMP/2d253969615725b1ea897a0b47e36b0e77d3f5e864d0308a2ba253a54df42fd4?placeholderIfAbsent=true&apiKey=48b4d741997c411b883c3a9cff6347e7",
    lab: "AI Laboratory",
    title: "Blog title heading will go here",
    description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse varius enim in eros."
  },
  // Repeat the above object 5 more times for a total of 6 items
];

function PublicationsPage() {
  return (
    <main className="flex flex-col">
      <Header />
      <section className="flex overflow-hidden flex-col items-center py-28 pr-11 pl-12 w-full bg-sky-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
        <div className="flex flex-col max-w-full text-center text-black w-[768px]">
          <h1 className="text-6xl font-bold leading-tight max-md:max-w-full max-md:text-4xl">
            Our Publications
          </h1>
          <p className="mt-6 text-lg max-md:max-w-full">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          </p>
        </div>
        <div className="flex gap-2 justify-center items-center py-2 pr-4 mt-20 text-base text-black pl-[1182px] max-md:pl-5 max-md:mt-10 max-md:max-w-full">
          <button className="flex gap-2 justify-center items-center self-stretch px-4 py-2 my-auto bg-white border border-black border-solid rounded-[34px]">
            <span className="self-stretch my-auto">Filter by Lab</span>
            <img loading="lazy" src="https://cdn.builder.io/api/v1/image/assets/TEMP/524365663c114c411d869366a9906005c5de50e51e65441ec6d4e98e6d430fbf?placeholderIfAbsent=true&apiKey=48b4d741997c411b883c3a9cff6347e7" alt="" className="object-contain shrink-0 self-stretch my-auto w-6 aspect-square" />
          </button>
        </div>
        <div className="flex flex-col self-stretch mt-20 w-full max-md:mt-10 max-md:max-w-full">
          <div className="flex flex-wrap gap-8 items-start w-full max-md:max-w-full">
            {publicationsData.map((publication, index) => (
              <PublicationCard key={index} {...publication} />
            ))}
          </div>
        </div>
      </section>
      <Footer />
    </main>
  );
}

export default PublicationsPage;