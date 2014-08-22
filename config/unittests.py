################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####                                                                                                                                        ####
####          UNITTEST SETTINGS FOR PLUGIN "hiddenService"                                                                                  ####
####                                                                                                                                        ####
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

maliciousHiddenServicePlugin_serviceDir='/opt/Tortazo/plugins/attack/utils/hiddenServiceTest'
maliciousHiddenServicePlugin_servicePort=8080
maliciousHiddenServicePlugin_hsserviceDir='/home/adastra/Escritorio/hidden_service_django'
maliciousHiddenServicePlugin_hsservicePort=80

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####                                                                                                                                        ####
####          UNITTEST SETTINGS FOR PLUGIN "bruter"                                                                                         ####
####                                                                                                                                        ####
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

bruterPlugin_Relay="88.20.30.40"
bruterPlugin_relayInvalid="INVALID"
bruterPlugin_portSSH=22
bruterPlugin_portHTTP=80
bruterPlugin_portFTP=21
bruterPlugin_portSNMP=161
bruterPlugin_portSMB=139
bruterPlugin_localportSMB=139
bruterPlugin_portInvalid=-1
bruterPlugin_dictFile='/opt/Tortazo/db/dictFileTest.txt'
bruterPlugin_dictFileInvalid='.|^*`+[]{}'
bruterPlugin_onionservice='xxxxxxxxxxxxxxxx.onion'
bruterPlugin_onionserviceInvalid='A1^09OADFGNY#()?.onion'
bruterPlugin_urlSite=":/.?.-/resource"

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####                                                                                                                                        ####
####          UNITTEST SETTINGS FOR PLUGIN "crawler"                                                                                        ####
####                                                                                                                                        ####
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

crawlerPlugin_regexInvalid="[INVALID REGEX"
crawlerPlugin_dictFileInvalid="INVALID FILE"
crawlerPlugin_urlSite=":/.?.-/resource"
crawlerPlugin_onionserviceInvalid='A1^09OADFGNY#()?.onion'
crawlerPlugin_portInvalid=-1

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####                                                                                                                                        ####
####          UNITTEST SETTINGS FOR PLUGIN "dirBruter"                                                                                      ####
####                                                                                                                                        ####
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

dirBruter_urlSite=":/.?.-/resource"
dirBruter_onionserviceInvalid='A1^09OADFGNY#()?.onion'
dirBruter_portInvalid=-1

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####                                                                                                                                        ####
####          UNITTEST SETTINGS FOR PLUGIN "stemming"                                                                                       ####
####                                                                                                                                        ####
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

stemming_queryTerms="hAckEr pOrN kIllER boYs GiRlS PiG"
stemming_onionserviceInvalid='A1^09OADFGNY#()?.onion'
stemming_portInvalid=-1

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
####                                                                                                                                        ####
####          UNITTEST SETTINGS FOR PLUGIN "shodan"                                                                                         ####
####                                                                                                                                        ####
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

shodan_apiKeyInvalid=''
shodan_apiKeyFileInvalid='INVALID SHODANKEY'
shodan_invalidLimit=-1
shodan_basicSearchInvalid=''
shodan_relayInvalid="INVALID"
shodan_nickNameInvalid=""