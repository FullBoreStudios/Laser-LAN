import React from 'react';
import {
  Image,
  StatusBar,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';
import {SafeAreaProvider, SafeAreaView} from 'react-native-safe-area-context';

const logoImage = require('./assets/images/logo.png');

function App() {
  return (
    <SafeAreaProvider>
      <SafeAreaView style={styles.safeArea}>
        <StatusBar
          barStyle="light-content"
          backgroundColor="#0b0f16"
        />
        <View style={styles.screen}>
          <View style={styles.gridOverlay} pointerEvents="none" />
          <View style={styles.glowPrimary} pointerEvents="none" />
          <View style={styles.glowSecondary} pointerEvents="none" />

          <View style={styles.content}>
            <Image source={logoImage} style={styles.logo} resizeMode="contain" />

            <View style={styles.hero}>
              <Text style={styles.kicker}>Arena Control</Text>
              <Text style={styles.title}>Match Access</Text>
              <Text style={styles.subtitle}>
                Sign in to manage rounds, monitor live state, and jump into the
                control dashboard.
              </Text>
            </View>

            <View style={styles.card}>
              <View style={styles.cardHighlight} />

              <View style={styles.fieldGroup}>
                <Text style={styles.label}>Username</Text>
                <TextInput
                  autoCapitalize="none"
                  autoCorrect={false}
                  placeholder="ENTER USERNAME"
                  placeholderTextColor="#5f6977"
                  style={styles.input}
                />
              </View>

              <View style={styles.fieldGroup}>
                <Text style={styles.label}>Password</Text>
                <TextInput
                  placeholder="ENTER PASSWORD"
                  placeholderTextColor="#5f6977"
                  secureTextEntry
                  style={styles.input}
                />
              </View>

              <View style={styles.button}>
                <Text style={styles.buttonText}>Login</Text>
              </View>

              <View style={styles.cardFooter}>
                <Text style={styles.footerText}>Custom auth flow</Text>
                <Text style={styles.footerLink}>Admin Dashboard</Text>
              </View>

              <View style={styles.cornerLeft} />
              <View style={styles.cornerRight} />
            </View>
          </View>
        </View>
      </SafeAreaView>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#0b0f16',
  },
  screen: {
    flex: 1,
    backgroundColor: '#0b0f16',
    overflow: 'hidden',
  },
  gridOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: '#0b0f16',
    opacity: 0.2,
    borderWidth: 0.5,
    borderColor: 'rgba(255, 255, 255, 0.02)',
  },
  glowPrimary: {
    position: 'absolute',
    top: '22%',
    left: '50%',
    width: 360,
    height: 360,
    marginLeft: -180,
    marginTop: -180,
    borderRadius: 180,
    backgroundColor: 'rgba(225, 29, 72, 0.22)',
    transform: [{scaleX: 1.15}],
  },
  glowSecondary: {
    position: 'absolute',
    bottom: -120,
    right: -40,
    width: 240,
    height: 240,
    borderRadius: 120,
    backgroundColor: 'rgba(190, 18, 60, 0.18)',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 24,
    paddingVertical: 32,
    gap: 22,
  },
  logo: {
    width: '100%',
    height: 220,
    alignSelf: 'center',
  },
  hero: {
    gap: 8,
    alignItems: 'center',
  },
  kicker: {
    color: '#6b7280',
    fontSize: 12,
    fontWeight: '700',
    letterSpacing: 3.5,
    textTransform: 'uppercase',
  },
  title: {
    color: '#f3f4f6',
    fontSize: 34,
    lineHeight: 38,
    fontWeight: '800',
    letterSpacing: 2.5,
    textTransform: 'uppercase',
    textAlign: 'center',
  },
  subtitle: {
    color: '#9ca3af',
    fontSize: 14,
    lineHeight: 21,
    textAlign: 'center',
    maxWidth: 320,
  },
  card: {
    position: 'relative',
    backgroundColor: 'rgba(19, 26, 38, 0.94)',
    borderWidth: 1,
    borderColor: '#1f2937',
    paddingHorizontal: 20,
    paddingTop: 26,
    paddingBottom: 18,
    gap: 16,
  },
  cardHighlight: {
    position: 'absolute',
    top: 0,
    left: 24,
    right: 24,
    height: 3,
    backgroundColor: '#e11d48',
    opacity: 0.95,
  },
  fieldGroup: {
    gap: 6,
  },
  label: {
    color: '#9ca3af',
    fontSize: 11,
    fontWeight: '700',
    letterSpacing: 2.2,
    textTransform: 'uppercase',
  },
  input: {
    backgroundColor: '#0b0f16',
    borderWidth: 1,
    borderColor: '#1f2937',
    color: '#f9fafb',
    paddingHorizontal: 14,
    paddingVertical: 14,
    fontSize: 14,
    letterSpacing: 1.2,
  },
  button: {
    marginTop: 4,
    backgroundColor: '#e11d48',
    paddingVertical: 15,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonText: {
    color: '#ffffff',
    fontSize: 17,
    fontWeight: '800',
    letterSpacing: 2.8,
    textTransform: 'uppercase',
  },
  cardFooter: {
    marginTop: 2,
    paddingTop: 6,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: 12,
  },
  footerText: {
    color: '#6b7280',
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 2.5,
    textTransform: 'uppercase',
    flexShrink: 1,
  },
  footerLink: {
    color: '#d1d5db',
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 1.8,
    textTransform: 'uppercase',
  },
  cornerLeft: {
    position: 'absolute',
    left: 0,
    bottom: 0,
    width: 12,
    height: 12,
    borderLeftWidth: 2,
    borderBottomWidth: 2,
    borderColor: '#6b7280',
  },
  cornerRight: {
    position: 'absolute',
    right: 0,
    bottom: 0,
    width: 12,
    height: 12,
    borderRightWidth: 2,
    borderBottomWidth: 2,
    borderColor: '#6b7280',
  },
});

export default App;
