function Eye() {
  return (
    <div className="relative shrink-0 size-[204px]" data-name="eye">
      <svg
        className="block size-full"
        fill="none"
        preserveAspectRatio="none"
        viewBox="0 0 204 204"
      >
        <g id="eye">
          <rect
            fill="var(--fill-0, #FBF0DC)"
            height="204"
            rx="102"
            width="204"
          />
          <circle
            cx="119.032"
            cy="117.787"
            fill="var(--fill-0, black)"
            id="Pupil"
            r="38"
          />
        </g>
      </svg>
    </div>
  );
}

function Eye1() {
  return (
    <div className="relative shrink-0 size-[204px]" data-name="eye">
      <svg
        className="block size-full"
        fill="none"
        preserveAspectRatio="none"
        viewBox="0 0 204 204"
      >
        <g id="eye">
          <rect
            fill="var(--fill-0, #FBF0DC)"
            height="204"
            rx="102"
            width="204"
          />
          <circle
            cx="74.8272"
            cy="78.3184"
            fill="var(--fill-0, black)"
            id="Pupil"
            r="38"
          />
        </g>
      </svg>
    </div>
  );
}

function Eyes() {
  return (
    <div className="relative shrink-0" data-name="eyes">
      <div className="box-border content-stretch flex flex-row gap-1 items-center justify-center p-0 relative">
        <Eye />
        <Eye1 />
      </div>
    </div>
  );
}

function Monster() {
  return (
    <div className="bg-[#0062ad] relative shrink-0" data-name="monster">
      <div className="flex flex-col items-center justify-center overflow-clip relative size-full">
        <div className="box-border content-stretch flex flex-col gap-2 items-center justify-center px-[22px] py-[117px] relative">
          <Eyes />
        </div>
      </div>
    </div>
  );
}

function Hero() {
  return (
    <div className="relative shrink-0 w-full" data-name="hero">
      <div className="box-border content-stretch flex flex-col items-start justify-start leading-[0] not-italic p-0 relative text-[#000000] text-left w-full">
        <div
          className="css-w9luqw font-['Inter:Bold',_sans-serif] font-bold min-w-full relative shrink-0 text-[64px]"
          style={{ width: "min-content" }}
        >
          <p className="block leading-[68px]">PANTONE</p>
        </div>
        <div
          className="css-w9luqw font-['Inter:Medium',_sans-serif] font-medium min-w-full relative shrink-0 text-[24px]"
          style={{ width: "min-content" }}
        >
          <p className="block leading-[normal]">Cookie Monster</p>
        </div>
      </div>
    </div>
  );
}

function Legend() {
  return (
    <div className="relative shrink-0 w-full" data-name="legend">
      <div className="relative size-full">
        <div className="box-border content-stretch flex flex-col gap-[55px] items-start justify-start px-0 py-[9px] relative w-full">
          <Hero />
          <div
            className="css-w9luqw font-['Inter:Medium',_sans-serif] font-medium leading-[0] min-w-full not-italic relative shrink-0 text-[#000000] text-[16px] text-left"
            style={{ width: "min-content" }}
          >
            <p className="block leading-[normal]">Sesame Street</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function Frame65() {
  return (
    <div className="bg-[#fbf0dc] relative shrink-0">
      <div className="flex flex-col justify-center overflow-clip relative size-full">
        <div className="box-border content-stretch flex flex-col gap-2 items-start justify-center p-[18px] relative">
          <Monster />
          <Legend />
        </div>
      </div>
    </div>
  );
}

export default function MonsterCard() {
  return (
    <div className="bg-[#0062ad] relative size-full" data-name="monster-card">
      <div className="flex flex-row items-center justify-center relative size-full">
        <div className="box-border content-stretch flex flex-row gap-2 items-center justify-center p-[132px] relative size-full">
          <Frame65 />
        </div>
      </div>
    </div>
  );
}
