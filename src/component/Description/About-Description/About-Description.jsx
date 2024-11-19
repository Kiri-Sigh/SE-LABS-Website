import React from "react";

import Quote from "./Quote";
import TableOfContents from "./Table-Of-Content";
import ContentSection from "./Content";
import "./About-Description.css";

const AboutDescription = () => {
  return (
    <main className="flex overflow-hidden flex-col justify-center px-36 pb-28 w-full text-black bg-gray-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
      <div className="flex flex-wrap gap-20 items-start w-full max-md:max-w-full">
        <TableOfContents />
        <article className="flex-1 flex flex-col text-base leading-6 min-w-[240px] max-md:max-w-full">
          <ContentSection title="Who are we?" id="heading-2" level={3}>
            <p className="pb-4 w-full max-md:max-w-full">
              Software engineering (SE) is an engineering discipline concerning
              all aspects of software production, including software analysis,
              design, development, testing, and deployment. SE requires profound
              abstract and logical thinking and the application of mathematics,
              logic, and computer science in order to produce efficient and
              reliable software with the available resources.
            </p>
          </ContentSection>
          <ContentSection
            title="Why Software Engineering?"
            id="heading-3"
            level={3}
          >
            <p className="pb-4 w-full max-md:max-w-full">
              It is hard to overstate the ubiquity of software nowadays. Every
              computer system is governed by software. Almost every human
              activity involves software in some form. Undoubtedly software
              industry is one of the largest and fastest growing industries in
              the world. Consequently, skilled software engineers are in high
              demand worldwide. As software becomes more and more complex, the
              programming skills and the rudimentary knowledge of software
              engineering that students obtained from traditional computer
              science and computer engineering curriculums are insufficient.
            </p>
            <p className="pb-4 w-full max-md:max-w-full">
              The development of real-world software applications requires the
              skills in analysing the problem domain and the customer's
              requirement and the skills in designing the software from the
              topmost level down to the implementation level. Moreover, a
              software engineer must be able to use proper tools, techniques,
              and methodologies in order to produce the software in an efficient
              manner.
            </p>
          </ContentSection>
          <ContentSection title="Missions and Values" id="heading-4" level={3}>
            <p className="pb-4 w-full max-md:max-w-full">
              Morbi sed imperdiet in ipsum, adipiscing elit dui lectus. Tellus
              id scelerisque est ultricies ultricies. Duis est sit sed leo nisl,
              blandit elit sagittis. Quisque tristique consequat quam sed. Nisl
              at scelerisque amet nulla purus habitasse.
            </p>
          </ContentSection>
          <ContentSection title="Leadership" id="heading-5" level={3}>
            <p className="pb-4 w-full max-md:max-w-full">
              Morbi sed imperdiet in ipsum, adipiscing elit dui lectus. Tellus
              id scelerisque est ultricies ultricies. Duis est sit sed leo nisl,
              blandit elit sagittis. Quisque tristique consequat quam sed. Nisl
              at scelerisque amet nulla purus habitasse.
            </p>
          </ContentSection>
          <Quote text='"Ipsum sit mattis nulla quam nulla. Gravida id gravida ac enim mauris id. Non pellentesque congue eget consectetur turpis. Sapien, dictum molestie sem tempor. Diam elit, orci, tincidunt aenean tempus."' />
          <ContentSection title="Faculty" id="heading-6" level={3}>
            <p className="pb-4 w-full max-md:max-w-full">
              Nunc sed faucibus bibendum feugiat sed interdum. Ipsum egestas
              condimentum mi massa. In tincidunt pharetra consectetur sed duis
              facilisis metus. Etiam egestas in nec sed et. Quis lobortis at sit
              dictum eget nibh tortor commodo cursus.
            </p>
          </ContentSection>
        </article>
      </div>
    </main>
  );
};

export default AboutDescription;
