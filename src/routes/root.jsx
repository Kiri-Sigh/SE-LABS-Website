import { Outlet, useNavigation } from "react-router-dom";
import Header from "../component/Header/Header";
import Footer from "../component/Footer/footer";
//import ThumbnailCard from "../component/etc/Thumbnail-test";

function RootLayout() {
  // const navigation = useNavigation();

  return (
    <>
      <Header />
      <main>
        {/* {navigation.state === 'loading' && <p>Loading...</p>} */}
        <Outlet />
      </main>
      <Footer />
    </>
  );
}

export default RootLayout;
