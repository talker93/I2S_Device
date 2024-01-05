# copy the modified file to overwrite its corresponding file
cp /ref/xk-audio-316-mc.xn ../testing/sw_usb_audio/app_usb_aud_xk_316_mc/src/core/xk-audio-316-mc.xn && \
cp /ref/xua_conf.h ../testing/sw_usb_audio/app_usb_aud_xk_316_mc/src/core/xua_conf.h && \
cp /ref/audiohw_ref.xc ../testing/sw_usb_audio/app_usb_aud_xk_316_mc/src/extensions/audiohw.xc && \
cp Makefile ../testing/sw_usb_audio/app_usb_aud_xk_316_mc/Makefile && \
cp main_dev.xc ../testing/lib_xua/lib_xua/src/core/main.xc && \
# go to the root and compile
cd ../testing/sw_usb_audio/app_usb_aud_xk_316_mc && pwd && \
	xmake CONFIG=2AMi2o2xxxxxx && \
	# copy binary to the target folder
	cd bin && cd 2AMi2o2xxxxxx && \
	cp app_usb_aud_xk_316_mc_2AMi2o2xxxxxx.xe ../../../../../bin



