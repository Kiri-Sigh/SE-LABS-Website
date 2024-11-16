import React from "react";

const Description = ({ data }) => {
  if (data) console.log(data);
  return (
    <section className="flex overflow-hidden flex-col justify-center px-16 py-28 w-full text-base leading-6 text-black bg-sky-100 max-md:px-5 max-md:py-24 max-md:max-w-full">
      <div className="flex flex-col w-full max-md:max-w-full">
        <h2 className="py-6 w-full text-4xl font-bold leading-tight whitespace-nowrap max-md:max-w-full">
          Introduction
        </h2>
        <p className="pb-4 w-full max-md:max-w-full">
          Mi tincidunt elit, id quisque ligula ac diam, amet. Vel etiam
          suspendisse morbi eleifend faucibus eget vestibulum felis. Dictum quis
          montes, sit sit. Tellus aliquam enim urna, etiam. Mauris posuere
          vulputate arcu amet, vitae nisi, tellus tincidunt. At feugiat sapien
          varius id.
        </p>
        <p className="pb-4 w-full max-md:max-w-full">
          Eget quis mi enim, leo lacinia pharetra, semper. Eget in volutpat
          mollis at volutpat lectus velit, sed auctor. Porttitor fames arcu quis
          fusce augue enim. Quis at habitant diam at. Suscipit tristique risus,
          at donec. In turpis vel et quam imperdiet. Ipsum molestie aliquet
          sodales id est ac volutpat.
        </p>
        <p className="pt-5 pb-4 w-full text-xl font-bold leading-7 max-md:max-w-full">
          Dolor enim eu tortor urna sed duis nulla. Aliquam vestibulum, nulla
          odio nisl vitae. In aliquet pellentesque aenean hac vestibulum turpis
          mi bibendum diam. Tempor integer aliquam in vitae malesuada fringilla.
        </p>
        <p className="pb-4 w-full max-md:max-w-full">
          Elit nisi in eleifend sed nisi. Pulvinar at orci, proin imperdiet
          commodo consectetur convallis risus. Sed condimentum enim dignissim
          adipiscing faucibus consequat, urna. Viverra purus et erat auctor
          aliquam. Risus, volutpat vulputate posuere purus sit congue convallis
          aliquet. Arcu id augue ut feugiat donec porttitor neque. Mauris, neque
          ultricies eu vestibulum, bibendum quam lorem id. Dolor lacus, eget
          nunc lectus in tellus, pharetra, porttitor.
        </p>
        <blockquote className="flex overflow-hidden items-start py-9 w-full text-xl leading-7 text-black max-md:max-w-full">
          <div className="flex overflow-hidden flex-wrap flex-1 shrink gap-5 pr-5 w-full basis-0 bg-white bg-opacity-0 min-w-[240px] max-md:max-w-full">
            <div className="flex shrink-0 w-0.5 h-14 bg-black" />
            <p className="flex-1 shrink self-start basis-0 max-md:max-w-full">
              "Ipsum sit mattis nulla quam nulla. Gravida id gravida ac enim
              mauris id. Non pellentesque congue eget consectetur turpis.
              Sapien, dictum molestie sem tempor. Diam elit, orci, tincidunt
              aenean tempus."
            </p>
          </div>
        </blockquote>
        <p className="pb-4 w-full max-md:max-w-full">
          Tristique odio senectus nam posuere ornare leo metus, ultricies.
          Blandit duis ultricies vulputate morbi feugiat cras placerat elit.
          Aliquam tellus lorem sed ac. Montes, sed mattis pellentesque suscipit
          accumsan. Cursus viverra aenean magna risus elementum faucibus
          molestie pellentesque. Arcu ultricies sed mauris vestibulum.
        </p>
        <h2 className="pt-6 pb-5 w-full text-3xl font-bold leading-tight whitespace-nowrap max-md:max-w-full">
          Conclusion
        </h2>
        <p className="pb-4 w-full max-md:max-w-full">
          Morbi sed imperdiet in ipsum, adipiscing elit dui lectus. Tellus id
          scelerisque est ultricies ultricies. Duis est sit sed leo nisl,
          blandit elit sagittis. Quisque tristique consequat quam sed. Nisl at
          scelerisque amet nulla purus habitasse.
        </p>
        <p className="pb-4 w-full max-md:max-w-full">
          Nunc sed faucibus bibendum feugiat sed interdum. Ipsum egestas
          condimentum mi massa. In tincidunt pharetra consectetur sed duis
          facilisis metus. Etiam egestas in nec sed et. Quis lobortis at sit
          dictum eget nibh tortor commodo cursus.
        </p>
        <p className="w-full max-md:max-w-full">
          Odio felis sagittis, morbi feugiat tortor vitae feugiat fusce aliquet.
          Nam elementum urna nisi aliquet erat dolor enim. Ornare id morbi eget
          ipsum. Aliquam senectus neque ut id eget consectetur dictum. Donec
          posuere pharetra odio consequat scelerisque et, nunc tortor. Nulla
          adipiscing erat a erat. Condimentum lorem posuere gravida enim posuere
          cursus diam.
        </p>
      </div>
    </section>
  );
};

export default Description;
