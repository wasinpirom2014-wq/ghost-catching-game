"""
Ad Manager - Handles Google AdMob integration
Supports Interstitial Ads and Rewarded Video Ads
"""

class AdManager:
    """
    Manages advertisement display and tracking
    
    For Android deployment with AdMob:
    - Interstitial Ads: Full-screen ads shown after level completion
    - Rewarded Video Ads: Short video ads that give in-game rewards
    """
    
    def __init__(self):
        self.interstitial_ad_unit_id = "ca-app-pub-1477667343771195/8396722467"  # Interstitial Ad (Level Complete)
        self.rewarded_ad_unit_id = "ca-app-pub-1477667343771195/8089600709"      # Rewarded Ad (Retry)
        self.is_ad_loaded = False
        self.ad_shown_count = 0
        self.reward_earned = False
    
    def set_ad_unit_ids(self, interstitial_id: str, rewarded_id: str):
        """
        Set the AdMob Ad Unit IDs
        
        Args:
            interstitial_id: Ad Unit ID for Interstitial Ads
            rewarded_id: Ad Unit ID for Rewarded Video Ads
        """
        self.interstitial_ad_unit_id = interstitial_id
        self.rewarded_ad_unit_id = rewarded_id
    
    def load_interstitial_ad(self):
        """Load an interstitial ad (full-screen ad)"""
        # This will be implemented in the Android/Kivy version
        # For now, this is a placeholder
        self.is_ad_loaded = True
    
    def show_interstitial_ad(self):
        """
        Show an interstitial ad after level completion
        
        In the actual Android app, this will:
        1. Display a full-screen advertisement
        2. Wait for the user to close it or for it to finish
        3. Return control to the game
        """
        if self.is_ad_loaded:
            self.ad_shown_count += 1
            self.is_ad_loaded = False
            self.load_interstitial_ad()
            return True
        return False
    
    def load_rewarded_video_ad(self):
        """Load a rewarded video ad"""
        self.is_ad_loaded = True
    
    def show_rewarded_video_ad(self):
        """
        Show a rewarded video ad
        
        Returns:
            bool: True if reward was earned (user watched the full video)
        """
        if self.is_ad_loaded:
            self.reward_earned = True
            self.is_ad_loaded = False
            self.load_rewarded_video_ad()
            return True
        return False
    
    def get_ad_stats(self) -> dict:
        """Get statistics about ads shown"""
        return {
            "ads_shown": self.ad_shown_count,
            "rewards_earned": self.reward_earned
        }

# Configuration for AdMob integration in buildozer.spec
ADMOB_CONFIG = """
# Google Play Services and AdMob
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# Required for AdMob
android.gradle_dependencies = com.google.android.gms:play-services-ads:20.6.0

# AdMob initialization code (to be added in main app)
"""

# Example implementation for Kivy (which will be used for Android build)
KIVY_ADMOB_EXAMPLE = """
from kivy.garden.mapview import MapView
from jnius import autoclass, cast

# Load AdMob classes
PythonJavaClass = autoclass('org.renpy.android.PythonJavaClass')
AdRequest = autoclass('com.google.android.gms.ads.AdRequest')
InterstitialAd = autoclass('com.google.android.gms.ads.interstitial.InterstitialAd')
RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
MobileAds = autoclass('com.google.android.gms.ads.MobileAds')

class AdManagerKivy:
    def __init__(self):
        # Initialize Mobile Ads SDK
        MobileAds.initialize(None)
        
        self.interstitial_ad = None
        self.rewarded_ad = None
    
    def load_interstitial(self, ad_unit_id):
        ad_request = AdRequest.Builder().build()
        InterstitialAd.load(
            self.context,
            ad_unit_id,
            ad_request,
            self.on_interstitial_loaded
        )
    
    def show_interstitial(self):
        if self.interstitial_ad:
            self.interstitial_ad.show(self.activity)
    
    def load_rewarded(self, ad_unit_id):
        ad_request = AdRequest.Builder().build()
        RewardedAd.load(
            self.context,
            ad_unit_id,
            ad_request,
            self.on_rewarded_loaded
        )
    
    def show_rewarded(self):
        if self.rewarded_ad:
            self.rewarded_ad.show(self.activity, self.on_user_earned_reward)
"""
