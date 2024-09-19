import { Outlet, useNavigation } from "react-router-dom";
import Footer from "../../component/footer";
import Header from "../../component/Header.jsx/Header";
import backgroundImage from "../../resources/background.webp";
function RootLayout() {
  // const navigation = useNavigation();

  return (
    <>
      <Header />
      <main>
        {/* {navigation.state === 'loading' && <p>Loading...</p>} */}

        <div
          style={{ backgroundImage: `url(${backgroundImage})` }}
          className="bg-container"
        >
          <Outlet className="content" />
        </div>
      </main>
      <Footer />
    </>
  );
}

export default RootLayout;
