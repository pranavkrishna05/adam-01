import Header from "./components/Header";
import Footer from "./components/Footer";
import AppRoutes from "./routes/AppRoutes";

const App = () => {
  return (
    <div className="app-layout">
      <Header />
      <main className="content">
        <AppRoutes />
      </main>
      <Footer />
    </div>
  );
};

export default App;
