# copy the modified file to overwrite its corresponding file
cp xk-audio-316-mc_nov_9.xn ../testing/sw_usb_audio/app_usb_aud_xk_316_mc/src/core/xk-audio-316-mc.xn && \
cp xua_conf_nov_9.h ../testing/sw_usb_audio/app_usb_aud_xk_316_mc/src/core/xua_conf.h && \
cp audiohw_nov_9.xc ../testing/sw_usb_audio/app_usb_aud_xk_316_mc/src/extensions/audiohw.xc && \
# go to the root and compile
cd ../testing/sw_usb_audio/app_usb_aud_xk_316_mc && pwd && \
	xmake CONFIG=2AMi2o2xxxxxx && \
	# copy binary to the target folder
	cd bin && cd 2AMi8o8xxxxxx && \
	cp app_usb_aud_xk_316_mc_2AMi2o2xxxxxx.xe ../../../../../bin



