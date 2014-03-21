(
s.boot;

//s.freqscope;
~net = NetAddr.new("127.0.0.1", 7001);
~audioPort = [3,4];
~innerPort = 420;

//~net.sendMsg("/bass", 1.0);
//~net.sendMsg("/test/alpha", 1.0);


{
	SynthDef(\Amp,{
		var in, amp;

		in = AudioIn.ar(~audioPort);

		amp = Slew.kr(Amplitude.kr(in),5,5);
		amp = Amplitude.kr(amp);

		SendReply.kr(Impulse.kr(30), "/amp", amp, ~innerPort);
	}).store;

	SynthDef(\Bass,{
		var in, bass;

		in = AudioIn.ar(~audioPort);

		bass = Slew.kr(Amplitude.kr(LPF.ar(in,110)),2,4);

		SendReply.kr(Impulse.kr(30), "/bass", bass*2, ~innerPort);
	}).store;

	SynthDef(\High,{
		var in, high;

		in = AudioIn.ar(~audioPort);

		high = Amplitude.kr(HPF.ar(in,1000));

		SendReply.kr(Impulse.kr(30), "/high", high, ~innerPort);
	}).store;

	SynthDef(\Note,{
		var in, freq, hasFreq;
		var note;

		in = AudioIn.ar(~audioPort);

		# freq, hasFreq = Pitch.kr(in, ampThreshold: 0.02, median: 7);

		// do=0, si=11/12
		note  = ( (log(freq)/log(2))-(log(16.35)/log(2)) ).mod(1);

		SendReply.kr(Impulse.kr(30), "/note", note, ~innerPort);
	}).store;

	s.sync;

	~ampS.free;
	~ampS = Synth(\Amp);

	~highS.free;
	~highS = Synth(\High);

	~bassS.free;
	~bassS = Synth(\Bass);

	~note.free;
	~note = Synth(\Note);
}.fork;


(~ampD.remove;
~ampD = OSCresponderNode(nil,"/amp",
	{
		| t, r, msg |
		~net.sendMsg("/amp",msg[3]);
	});
).add;

(~highD.remove;
~highD = OSCresponderNode(nil,"/high",
	{
		| t, r, msg |
		~net.sendMsg("/high",msg[3]);
	});
).add;

(~bassD.remove;
~bassD = OSCresponderNode(nil,"/bass",
	{
		| t, r, msg |
		~net.sendMsg("/bass",msg[3]);
	});
).add;

(~noteD.remove;
~noteD = OSCresponderNode(nil,"/note",
	{
		| t, r, msg |
		~net.sendMsg("/note",msg[3]);
	});
).add;
)