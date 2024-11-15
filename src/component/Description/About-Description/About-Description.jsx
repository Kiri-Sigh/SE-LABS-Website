import React from "react";

import Quote from "./Quote";
import TableOfContents from "./Table-Of-Content";
import ContentSection from "./Content";

const AboutDescription = () => {
  return (
    <main className="flex overflow-hidden flex-col justify-center px-36 py-28 w-full text-black bg-sky-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
      <div className="flex flex-wrap gap-10 justify-between items-start w-full max-md:max-w-full">
        <TableOfContents />
        <article className="flex flex-col text-base leading-6 min-w-[240px] w-[768px] max-md:max-w-full">
          <ContentSection title="Heading 2" level={2}>
            <p className="pb-4 w-full font-bold max-md:max-w-full">
              Dolor enim eu tortor urna sed duis nulla. Aliquam vestibulum,
              nulla odio nisl vitae. In aliquet pellentesque aenean hac
              vestibulum turpis mi bibendum diam. Tempor integer aliquam in
              vitae malesuada fringilla.
            </p>
            <p className="pb-4 w-full max-md:max-w-full">
              Mi tincidunt elit, id quisque ligula ac diam, amet. Vel etiam
              suspendisse morbi eleifend faucibus eget vestibulum felis. Dictum
              quis montes, sit sit. Tellus aliquam enim urna, etiam. Mauris
              posuere vulputate arcu amet, vitae nisi, tellus tincidunt. At
              feugiat sapien varius id.
            </p>
          </ContentSection>
          <ContentSection title="Heading 3" level={3}>
            <p className="pb-4 w-full max-md:max-w-full">
              Eget quis mi enim, leo lacinia pharetra, semper. Eget in volutpat
              mollis at volutpat lectus velit, sed auctor. Porttitor fames arcu
              quis fusce augue enim. Quis at habitant diam at. Suscipit
              tristique risus, at donec. In turpis vel et quam imperdiet. Ipsum
              molestie aliquet sodales id est ac volutpat.
            </p>
            <p className="pb-4 w-full max-md:max-w-full">
              Tristique odio senectus nam posuere ornare leo metus, ultricies.
              Blandit duis ultricies vulputate morbi feugiat cras placerat elit.
              Aliquam tellus lorem sed ac. Montes, sed mattis pellentesque
              suscipit accumsan. Cursus viverra aenean magna risus elementum
              faucibus molestie pellentesque. Arcu ultricies sed mauris
              vestibulum.
            </p>
          </ContentSection>
          <ContentSection title="Heading 4" level={4}>
            <p className="pb-4 w-full max-md:max-w-full">
              Morbi sed imperdiet in ipsum, adipiscing elit dui lectus. Tellus
              id scelerisque est ultricies ultricies. Duis est sit sed leo nisl,
              blandit elit sagittis. Quisque tristique consequat quam sed. Nisl
              at scelerisque amet nulla purus habitasse.
            </p>
          </ContentSection>
          <ContentSection title="Heading 5" level={5}>
            <p className="pb-4 w-full max-md:max-w-full">
              Morbi sed imperdiet in ipsum, adipiscing elit dui lectus. Tellus
              id scelerisque est ultricies ultricies. Duis est sit sed leo nisl,
              blandit elit sagittis. Quisque tristique consequat quam sed. Nisl
              at scelerisque amet nulla purus habitasse.
            </p>
          </ContentSection>
          <Quote text='"Ipsum sit mattis nulla quam nulla. Gravida id gravida ac enim mauris id. Non pellentesque congue eget consectetur turpis. Sapien, dictum molestie sem tempor. Diam elit, orci, tincidunt aenean tempus."' />
          <ContentSection title="Heading 6" level={6}>
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
