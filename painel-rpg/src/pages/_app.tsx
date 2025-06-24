import "../styles/globals.css";
import { AuthProvider } from "../context/AuthContext";
import "../i18n";

function MyApp({ Component, pageProps }) {
  return (
    <AuthProvider>
      <Component {...pageProps} />
    </AuthProvider>
  );
}
export default MyApp;
